from bs4 import BeautifulSoup
import glob
import os
import sys 
from pymarc import MARCReader, record_to_xml
import re
import numpy as np
import pandas as pd


EAD_FIELD_TO_BS_SELECTOR_MAPPING = {
    'identifier': 'eadid',
    'finding_aid_title':'titleproper',
    'acquisition_number':'num',
    'finding_aid_creator': 'author',
    'repository':'repository > corpname',
    'publisher': 'publisher',
    'date_of_publication':'publicationstmt>date',
    'date_of_creation': 'profiledesc > creation > date',
    'collection_title': 'archdesc[\'level\'=\'collection\'] > did > unittitle',
    # one or many
    'extent': 'physdesc > extent',
    'temporal_coverage': 'archdesc[\'level\'=\'collection\'] > did > unitdate',
    # one or many, 1 child per
    'collection_creator': 'origination[\'label\'=\'creator\'] > *',
    'conditions_governing_use': 'userestrict > p',
    # one or many, one p per
    'related material': 'relatedmaterial > p',
    # one or many
    'collection_scope_and_content': 'archdesc > scopecontent > p',
    # has em tags, one or many)
    'biography_or_history': 'bioghist > p',
    'preferred_citation': 'prefercite > p',
    'subject_headings': 'controlaccess > *',
    ### get c01 - c09, walk down series, subseries, and otherlevel
    # get did> unitid , did> unittitle
    # scopecontent > p (one or many)
    # series_type is level attribute
    #'series_titles':,
    #series_numbers':,
    #'series_types':,
    #'series_scope_and_content':,
}

MODS_FIELD_TO_BS_SELECTOR_MAPPING = {
    'title':'mods\:mods > mods\:titleInfo > mods\:title',
    'identifier': 'mods\:identifier[type=\"pitt\"]',
    'creator': 'mods\:name', # will need additional filtering
    'date': 'mods\:originInfo > mods\:dateCreated',
    'depositor': 'mods\:name', # will need additional filtering
    'box': 'mods\:note[type=\"container\"]', # this will need additional parsing
    'folder': 'mods\:note[type=\"container\"]', # this willneed additional parsing
    'type_of_resource': 'mods\:typeOfResource',
    'genre': 'mods\:genre',
}

def clean_field(field_key, field_data):
    if field_key == 'box':
        for i,field_string in enumerate(field_data):
            m = re.search('Box (\d*),', field_string)
            field_data[i] = m.group(0)
        return field_data
    elif field_key == 'folder':
        for i,field_string in enumerate(field_data):
            m = re.search('Folder (\d*)', field_string)
            field_data[i] = m.group(0)
        return field_data

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
            field_data = bs_object.select(field_dict[u])
            field_data = [e.text.strip() for e in field_data]
        except:
            #respond if it errors or is empty
            field_data = ''
        # parse field if needed ... with conditionals
        # field_data = clean_field(u, field_data)
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
    #write row to yml file

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
        row = get_fields_from_bs(x, EAD_FIELD_TO_BS_SELECTOR_MAPPING)
        collection_record_dict = {}
        for key in row.keys():
            collection_record_dict[key] = (row[key])
        collection_output_rows.append(collection_record_dict)

    item_data = get_bs_from_xml(item_dir, 'mods')
    item_output_rows = []
    for x in item_data:
        row = get_fields_from_bs(x, MODS_FIELD_TO_BS_SELECTOR_MAPPING)
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
