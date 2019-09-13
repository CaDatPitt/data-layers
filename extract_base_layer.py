from bs4 import BeautifulSoup
import glob
import os
import sys
from pymarc import MARCReader, record_to_xml
import re
import numpy as np
import pandas as pd
import data_layers_config


def get_fields_from_bs(bs_object, field_dict):
    """
    Takes two arguments:
    1) a BeautifulSoup object
    2) a dictionary of fields with bs.find arguments as values and/or findall
    Returns a dictionary of matching field values
    """
    row = {}
    for u in field_dict.keys():
        try:
            field_list = []
            for e in bs_object.select(field_dict[u]['bs_exp']):
                s = e.text.replace("\n", " ").replace("\t", " ")
                joined_s = " ".join(s.split())
                field_list.append(joined_s)
            field_data = "; ".join(field_list)
            #field_data = [e.text for e in bs_object.select(field_dict[u])]
        except:
            #respond if it errors or is empty
            field_data = ''
        
        # try to get field_dict[u]['helper_funct'], use root_param value for conditional, use getattr to retrieve
        try:
            function = getattr(field_dict[u]['helper_funct'])
            if field_dict[u]['root_param'] == 'bs':
                lead_arg = bs_object
            elif field_dict[u]['root_param'] == 'text':
                lead_arg = field_data
            
            field_data = funtion(lead_arg, field_dict[u]['args'] )
        except:
            pass

        row[u] = field_data


    return row

def get_bs_from_xml(_dir, source_type):
    """
    Reads source data files and returns list of BeautifulSoup objects
    Requires file type argument, one of ead, mods, or marc binary
    """
    if source_type == 'marc':
        filenames = glob.glob(_dir + '*.mrc')
    if source_type == 'mods' or source_type == 'ead':
        filenames = glob.glob(_dir + '*.xml')

    print("working with %d %s files" % (len(filenames), source_type))

    bs_objects = []
    for z in filenames:
        # if file type is marc binary, use pymarc to convert to xml
        if source_type == 'marc':
            with open(z, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    xml = record_to_xml(record).decode("utf-8")
        # if file type is mods or ead, we assume it's already xml
        if source_type == 'mods' or source_type == 'ead':
            with open(z, encoding="utf-8") as f:
                xml = f.read()
        bs = BeautifulSoup(xml, "lxml")
        bs_objects.append(bs)

    return bs_objects

def create_data_frame_from_list(source_list):
    # we assume that each list item is a dictionary of key/value pairs.
    # create a dictionary of numpy Series objects; then pass this to pandas DataFrame constructor
    # transpose data frame to get expected record-based orientation
    d = {}
    for i, row in enumerate(source_list):
        d[i] = pd.Series(row)
    return pd.DataFrame(d).T

def get_name_by_type(bs_object, role):
    """
    This function accepts a BeautifulSoup object and a role, which is a string. 
    It parses the xml object and returns the string value if the role matches. 
    Otherwise it returns None
    """
    if bs_object.find('mods\:roleTerm').text.lower().strip() == role.lower().strip():
        names = bs_object.find_all('mods\:namePart')
        name = "; ".join([y.text for y in names])
        return name
    else:
        return ""

def parse_container(container_desc, container_type):
    """ 
    We pass this a natural language container description, 
    use the container_type (e.g. 'folder') as a regex needle, match text directly after, 
    and return a substring based on the result
    Example: Box 1, folder 1
    """
    base_needle = '\s?(\d+)\D?'
    needle = container_type.lower()+base_needle
    try:
        matches = re.search(needle, container_desc.lower())
        match = matches.group(0)
    except: 
        match = ""
    return match

def base_layer_maker(location, collection_type, collection_subtype):
    """
    This function accepts three arguments and writes data to base-layers
    Location should be a folder name only that can be found in source-data, such as 'american-left-ephemera'
    collection_type is a controlled vocabulary ('archive', 'serial', 'monograph') ... errors if you pass anything else
    collection_subtype is 'digital' or 'print'
    """
    # some validation of arguments
    if not os.path.exists('source-data/%s' % location):
        raise Exception ("location source-data/%s not found!" % (location,))

    if collection_type not in ['archive', 'serial', 'monograph']:
        raise Exception ("collection type '%s' not one of 'archive', 'monograph', or 'serial'." % (collection_type,))

    if collection_subtype not in ['digital', 'print']:
        raise Exception ("collection subtype '%s' not one of 'digital', 'print'." % (collection_subtype,))

    # route source data processing based on type
    result = {}
    if collection_type == 'archive':
        collection_dir = "source-data/%s/ead/" % location
        if not os.path.exists(collection_dir):
            raise Exception ("location %s not found!" % (collection_dir,))
        item_dir = "source-data/%s/mods/" % location
        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))
        [coll_list, item_list] = process_archive_source_data(collection_dir, item_dir)

    elif collection_type == 'serial':
        [coll_list, item_list] = process_archive_source_data(location)

    elif collection_type == 'monograph':
        [coll_list, item_list] = process_monograph_source_data(location)

    #convert output_rows to pandas dataframe and use to_csv()
    #write row to yml or md file

    coll_df = create_data_frame_from_list(coll_list)
    item_df = create_data_frame_from_list(item_list)

    #create subdirectory in base-layers for that location
    newdir = "base-layers/" + location
    try:
        os.stat(newdir)
    except:
        os.mkdir(newdir)

    coll_csv = open(newdir + "/collection-base-layer.csv", 'w')
    coll_csv.write(coll_df.to_csv())
    coll_csv.close()

    item_csv = open(newdir + "/item-base-layer.csv", 'w')
    item_csv.write(item_df.to_csv())
    item_csv.close()
    print("success!")
    return

def process_archive_source_data(collection_dir, item_dir):

    collection_data = get_bs_from_xml(collection_dir, 'ead')
    collection_output_rows = []
    for x in collection_data:
        row = get_fields_from_bs(x, data_layers_config.EAD_MAP)
        collection_record_dict = {}
        for key in row.keys():
            collection_record_dict[key] = (row[key])
        collection_output_rows.append(collection_record_dict)

    item_data = get_bs_from_xml(item_dir, 'mods')
    item_output_rows = []
    for x in item_data:
        row = get_fields_from_bs(x, data_layers_config.MODS_MAP)
        item_record_dict = {}
        for key in row.keys():
            item_record_dict[key] = row[key]
        item_output_rows.append(item_record_dict)

    return collection_output_rows, item_output_rows


def process_serial_source_data(location):
    return

def process_monograph_source_data(location):
    return

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('when running as a script, you must provide three arguements: source collection name, collection type, and collection sub-type')
    base_layer_maker(sys.argv[1], sys.argv[2], sys.argv[3])
