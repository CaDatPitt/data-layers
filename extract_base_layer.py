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
    exceptions = ['creator', 'depositor', 'box'  'folder', 'copyright_status']

    for u in field_dict.keys():

        if u not in exceptions:
            field_list = []
            results = bs_object.select(field_dict[u]['bs_exp'])
            for e in results:   
                s = e.text.replace("\n", " ").replace("\t", " ")
                joined_s = " ".join(s.split())
                field_list.append(joined_s)
            field_data = "; ".join(field_list)
        if u == 'creator' or u == 'depositor':            
            field_data = get_name_by_type(bs_object, u)

        if u == 'copyright_status':
            results = bs_object.select(field_dict[u]['bs_exp'])
            try:
                field_data = results[0]['copyright.status']
            except:
                field_data = ''

        if u == 'box' or u == 'folder':
            results = bs_object.select(field_dict[u]['bs_exp'])
            field_list = [parse_container(z.text, u) for z in results]
            field_data = "; ".join(field_list)

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
                    bs = BeautifulSoup(xml, "xml")
                    bs_objects.append(bs)
        # if file type is mods or ead, we assume it's already xml
        if source_type == 'mods' or source_type == 'ead':
            with open(z, encoding="utf-8") as f:
                xml = f.read()

            bs = BeautifulSoup(xml, "xml")
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
    
    # this has to be a find_all because sometimes the file has multiple roleTerm elements
    # and the one we want is second, third, nth
    role_term = bs_object.find_all('roleTerm')
    for r in role_term:
        if role == 'depositor':
            if r.text.lower().strip() == role.lower().strip():
                
                names = bs_object.find_all('namePart')
                name = "; ".join([y.text for y in names])
                #once we've found the right roleTerm, we need not search the rest
                return name
            else:
                pass
        name = ""
        if role == 'creator':
            if r.text.lower().strip() != 'depositor':
                names = bs_object.find_all('namePart')
                names_filtered = []
                for i in names:
                    try:
                        if i['type'] == 'date':
                            pass
                        else:
                            names_filtered.append(i)
                    except:
                        names_filtered.append(i)
                
                name = "; ".join([y.text for y in names_filtered])
                #once we've found the right roleTerm, we need not search the rest
                return name

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
        match = matches.group(1)
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
        item_dir = "source-data/%s/mods/" % location
        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))

        [coll_list, item_list] = process_serial_source_data(item_dir)

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
        row = get_fields_from_bs(x, data_layers_config.ARCHIVAL_ITEM_MODS_MAP)
        item_record_dict = {}
        for key in row.keys():
            item_record_dict[key] = row[key]
        item_output_rows.append(item_record_dict)

    return collection_output_rows, item_output_rows


def process_serial_source_data(location):
    collection_output_rows = []
    item_data = get_bs_from_xml(location, 'mods')

    item_output_rows = []
    for x in item_data:
        row = get_fields_from_bs(x, data_layers_config.SERIAL_ITEM_MODS_MAP)
        item_record_dict = {}
        for key in row.keys():
            item_record_dict[key] = row[key]
        item_output_rows.append(item_record_dict)

    return collection_output_rows, item_output_rows

def process_monograph_source_data(location):
    return

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('when running as a script, you must provide three arguements: source collection name, collection type, and collection sub-type')
    base_layer_maker(sys.argv[1], sys.argv[2], sys.argv[3])
