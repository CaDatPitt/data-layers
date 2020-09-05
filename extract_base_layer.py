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
    exceptions = ['creator', 'contributor', 'depositor', 'copyright_status', 'genre', 'type_of_resource']

    for u in field_dict.keys():
        #assumes field_dict[u]['bs_exp'] is a list of expressions
        expressions = field_dict[u]['bs_exp']

        field_data = ""

        for exp in expressions:
            if u not in exceptions:
                bs_list = []
                results = bs_object.select(exp)
                for e in results:   
                    s = e.text.replace("\n", " ").replace("\t", " ")
                    joined_s = " ".join(s.split())
                    bs_list.append(joined_s)
                field_list = omit_repeats(bs_list)
                field_data += "; ".join(field_list)

            if u == 'creator' or u == 'contributor' or u == 'depositor': 
                results = bs_object.select(exp)
                # get multiple values, look for a grandchild, check value, then get namePart child text 
                for r in results:
                    this_data = get_name_by_grand_child(r, 'role > roleTerm', u, 'namePart' ) 
                    field_data += this_data
                    if this_data != "":
                        field_data += "; "
                if field_data[-2:] == "; ":
                    field_data = field_data[0:-2]

            if u == 'copyright_status':
                # looks for attribute value and handles exception if no attribute
                results = bs_object.select(exp)
                try:
                    field_data += results[0]['copyright.status']
                except:
                    field_data += ''
        
            if u == 'genre' or u == 'type_of_resource':
                # handles multiple results and omits repeats
                results = bs_object.select(exp)
                bs_list = [u.text for u in results]
                field_list = omit_repeats(bs_list)
                field_data += "; ".join(field_list)

        row[u] = field_data
        
    return row

def omit_trailing_punct(text):
    if len(text) > 0:
        if text[-1] in ['.', ',', ';']:
            text = text[0:-1]
    return text

def omit_repeats(text_list):
    try:
        lowered = [omit_trailing_punct(u.lower().strip()) for u in text_list]
        lowered_no_repeats = list(set(lowered))
        lowered_no_repeats.sort()
        return lowered_no_repeats
    except:
        return text_list

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

def get_name_by_grand_child(bs_object, grand_child_exp, grand_child_element_value, children='namePart' ):
    """
    This function accepts a BeautifulSoup object, find role > roleTerm="creator", "depositor", or 
    "contributor", and then if it matches, we return all namePart element values, comma separated
    """

    # matches where roleTerm = grand_child_element_value
    grand_children = bs_object.select(grand_child_exp)

    all_matches_joined = ""
    
    match = False
    for g in grand_children:

        if g.text == grand_child_element_value:
            match = True
            break
    if match:
        all_matches = bs_object.select(children)
        all_matches_joined += ", ".join([i.text for i in all_matches])
        
    # matches where there is no role, and grand_child_element_value=contributor
    if grand_child_element_value == 'contributor':
        no_roles = bs_object.select('role')
        if len(no_roles) == 0:
            all_matches = bs_object.select(children)
            all_matches_joined += ", ".join([i.text for i in all_matches])
    return all_matches_joined


def get_name_by_type(bs_object, role):
    """
    This function accepts a BeautifulSoup object and a role, which is a string. 
    It parses the xml object and returns the string value if the role matches. 
    Otherwise it returns None
    """
    
    # this has to be a find_all because sometimes the file has multiple roleTerm elements
    # and the one we want is second, third, nth
    names = bs_object.find_all('name')
    names_all = []
    
    for n in names:
        role_match = n.find('role')
        namePart = n.find('namePart') 
        if role_match:
            if role_match.text.lower().strip() == role:
                names_all.append(namePart.text)
                
    field_list = omit_repeats(names_all)
    if len(field_list) > 0:
        name = "; ".join(field_list)
    else:
        name = ""
    return name

def base_layer_maker(location, collection_type, collection_subtype):
    """
    This function accepts three arguments and writes data to base-layers
    Location should be a folder name only that can be found in source-data, such as 'american-left-ephemera'
    collection_type is a controlled vocabulary ('archival', 'serial', 'monograph') ... errors if you pass anything else
    collection_subtype is 'digital' or 'print'
    """
    # some validation of arguments
    if not os.path.exists('source-data/%s' % location):
        raise Exception ("location source-data/%s not found!" % (location,))

    if collection_type not in ['archival', 'serial', 'monograph']:
        raise Exception ("collection type '%s' not one of 'archive', 'monograph', or 'serial'." % (collection_type,))

    if collection_subtype not in ['digital', 'print']:
        raise Exception ("collection subtype '%s' not one of 'digital', 'print'." % (collection_subtype,))

    # route source data processing based on type
    result = {}
    if collection_type == 'archival':
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
        item_dir = "source-data/%s/marc_mods/" % location

        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))

        [coll_list, item_list] = process_monograph_source_data(item_dir)

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
    collection_output_rows = []
    item_data = get_bs_from_xml(location, 'mods')

    item_output_rows = []

    for f in item_data:
        for x in f.find_all('mods'):
            row = get_fields_from_bs(x, data_layers_config.MONOGRAPH_ITEM_MODS_MAP)
            item_record_dict = {}
            for key in row.keys():
                item_record_dict[key] = row[key]
            item_output_rows.append(item_record_dict)

    return collection_output_rows, item_output_rows

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('when running as a script, you must provide three arguments: source collection name, collection type, and collection sub-type')
    base_layer_maker(sys.argv[1], sys.argv[2], sys.argv[3])
