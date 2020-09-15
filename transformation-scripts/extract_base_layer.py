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
    Parses and extracts data from XML to populate CSV fields.

    Parameters
    -----------
    bs_object: bs4.BeautifulSoup
        a BeautifulSoup object
    field_dict: dict
        a dictionary of fields with bs.find arguments as values and/or findall
    Returns
    -------
    row: dict
        a dictionary of matching field values
    """

    row = {}
    exceptions = ['title', 'associated_name', 'creator', 'contributor', 'depositor', 'publisher',
    'encoded_date', 'publication_date', 'genre', 'type_of_resource', 'copyright_status', 'collection_language']

    for key in field_dict.keys():
        #assumes field_dict[key]['bs_exp'] is a list of expressions
        expressions = field_dict[key]['bs_exp']
        field_data = ""

        for exp in expressions:
            if key not in exceptions:
                field_list = []
                results = bs_object.select(exp)

                for result in results:
                    value = result.text.replace("\n", " ").replace("\t", " ").strip()
                    joined_value = " ".join(value.split())
                    if joined_value != "" and omit_repeats(joined_value, field_list):
                        field_list.append(joined_value)
                field_data += "|||".join(field_list)

            if key == 'title':
                results = bs_object.select(exp)
                title_value, subTitle_value, nonSort_value = "", "", ""
                # check titleInfo child element name and get element value
                # concatenate any appropriate punctuation for formatting purposes
                for result in results:
                    if result.name == 'title':
                        title_value = result.text.strip()
                    if result.name == 'subTitle':
                        if result.text != "" and (result.text)[0] == "(":
                            subTitle_value = " " + result.text.strip()
                        else:
                            subTitle_value = ": " + result.text.strip()
                    if result.name == 'nonSort':
                        nonSort_value = ", " + result.text.strip()
                # concatenate child element values with appropriate formatting
                field_data += title_value + subTitle_value + nonSort_value

            if key == 'associated_name' or key == 'creator' or key == 'contributor' or key == 'depositor':
                results = bs_object.select(exp)
                value = ""
                field_list = []
                # get multiple values, look for a grandchild, check value, then get namePart child text
                for result in results:
                    value = get_name_by_grand_child(result, key, 'namePart', 'role > roleTerm')
                    if value != "" and omit_repeats(value, field_list):
                        field_list.append(value)
                field_data += "|||".join(field_list)

            if key == 'publisher':
                results = bs_object.select(exp)
                field_list = []

                for result in results:
                    value = ""
                    if result.name == 'publisher':
                        value = result.text.strip()
                    else:
                        value = get_name_by_grand_child(result, key, 'namePart', 'role > roleTerm')
                    joined_value = " ".join(value.split())
                    if joined_value != "":
                        field_data += "|||" + joined_value
                field_data = field_data.strip('|||')

            if key == 'encoded_date':
                results = bs_object.select(exp)
                start_value, end_value, other_value = "", "", ""

                for result in results:
                    if result.has_attr('point'):
                        if result['point'] == "start":
                            start_value = result.text.strip()
                        else:
                            end_value += "/" + result.text.strip()
                    if not(result.has_attr('point')):
                       other_value = "|||" + result.text.strip()
                       if other_value != "":
                           field_data += "|||" + other_value
                if start_value != "" or end_value != "":
                    field_data += "|||" + start_value + end_value
                field_data = field_data.strip('|||')

            if key == 'publication_date':
                results = bs_object.select(exp)
                value = ""
                field_list = []
                #
                for result in results:
                    if not(result.attrs):
                        value = result.text.strip()
                        joined_value = " ".join(value.split())
                        if joined_value != "" and omit_repeats(joined_value, field_list):
                            field_list.append(joined_value)
                field_data += "|||".join(field_list)

            if key == 'copyright_status':
                results = bs_object.select(exp)
                # looks for attribute value and handles exception if no attribute
                for result in results:
                    try:
                        field_data += results[0]['copyright.status']
                    except:
                        field_data += ''

            if key == 'collection_language':
                results = bs_object.select(exp)
                # looks for attribute value and handles exception if no attribute
                for result in results:
                    try:
                        field_data += results[0]['langcode']
                    except:
                        field_data += ''

            if key == 'genre' or key == 'type_of_resource':
                results = bs_object.select(exp)
                value = ""
                field_list = []
                # handles multiple result and omits repeats
                for result in results:
                    value = omit_trailing_punct((result.text).strip())
                    if value != "" and omit_repeats(value, field_list):
                        field_list.append(value)
                field_list.sort()
                field_data += "|||".join(field_list)

        row[key] = field_data

    return row

def get_name_by_grand_child(bs_object, key, children='namePart', grand_child_exp='role > roleTerm'):
    """
    Extract and processes namePart element values and, in specified cases, roleTerm element values.

    Parameters
    -----------
    bs_object: bs4.BeautifulSoup
        a BeautifulSoup object
    grand_child_exp: str
        a specified node in a CSS selector expression ('role > roleTerm')
    key: str
        a specified key in the field_dict dictionary ('asssociated_name', 'contributor',
        'creator', 'depositor', or 'publisher')
    children: str
        a specified node in a CSS selector expression ('namePart')

    Returns
    -------
    name_parts_joined: str
        matched and processed namePart element values (comma-separated)
        and, sometimes, roleTerm element values (in parentheses)
    """

    name_tags = bs_object
    namePart_tags = bs_object.select(children)
    roleTerm_tags = bs_object.select(grand_child_exp)
    specified_roleTerms = [['author', 'authors', 'aut', 'composer', 'composers', 'cmp',
    'creator', 'creators', 'cre', 'dubious author', 'dub', 'editor', 'editors', 'edt',
    'joint author', 'joint authors', 'screenwriter', 'aus','supposed author', 'supposed authors'],
    ['publisher', 'publishers', 'pbl'], ['depositor']]
    creator, publisher, depositor = specified_roleTerms[0], specified_roleTerms[1], specified_roleTerms[2]
    matched_roleTerm_list = []
    name_parts_joined = ""
    match = False

    # matches where roleTerm value is in the appropriate sublist of specified_roleTerms, based on key
    if name_tags.role:
        for tag in roleTerm_tags:
                roleTerm_value = tag.text
                if key == 'creator':
                    if roleTerm_value in creator:
                        match = True
                elif key == 'depositor':
                    if roleTerm_value in depositor:
                        match = True
                elif key == 'publisher':
                    if roleTerm_value in publisher:
                        match = True
                elif key == 'contributor':
                    if not(any(roleTerm_value in sublist for sublist in specified_roleTerms)):
                        match = True
                        matched_roleTerm_list.append(roleTerm_value)
                elif key == 'associated_name':
                    if roleTerm_value not in 'depositor':
                        match = True
                        if roleTerm_value.strip() != "":
                            matched_roleTerm_list.append(roleTerm_value)
                else:
                    pass
    # matches where no role exists
    else:
        if key == 'creator' and bs_object.has_attr('usage'):
            match = True
        elif key == 'contributor' and not(bs_object.has_attr('usage')):
            match = True
        else:
            pass
    # if roleTerm matches key, concatenates all namePart values, separated by a comman
    # if key is 'associated name' or 'contributor', also concatenates roleTerm values in parentheses
    if match:
        name_parts_joined += ", ".join([i.text.replace("\n", " ").replace("\t", " ").strip() for i in namePart_tags])
        if key == 'contributor' or key == 'associated_name' and name_tags.role and matched_roleTerm_list:
            matched_roleTerms = ", ".join(matched_roleTerm_list)
            name_parts_joined += " (" + matched_roleTerms + ")"

    return name_parts_joined

def omit_trailing_punct(text):
    """
    Checks if a value already exists in a list.

    Parameters
    -----------
    text: str
        (processed) text from a bs.find result

    Returns
    -------
    text: str
         text with specified trailing punctuation removed, if any
    """

    if len(text) > 0:
        if text[-1] in ['.', ',', ';']:
            text = text[0:-1]
    return text

def omit_repeats(value, field_list):
    """
    Checks if a value already exists in a list.

    Parameters
    -----------
    value: str
        processed text from a bs.find result

    Returns
    -------
    boolean
         True if the value is not already in the list; False if it is
    """

    value = value.lower()
    field_list = [i.lower() for i in field_list]
    if value in field_list:
        return False
    else:
        return True

def get_bs_from_xml(_dir, source_type):
    """
    Reads source data files and returns list of BeautifulSoup objects.

    Parameters
    -----------
    _dir: str
        the path to a directory
    source_type: str
        the type of a source data file ('mods', 'marc', or 'mods')

    Returns
    -------
    bs_objects: list
         a list of BeautifulSoup objects
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
    """
    Creates a pandas DataFrame from a list of dictionaries.

    Parameters
    -----------
    source_list: list
        a list of dictionaries containing extracted and processed source data (key/value pairs)

    Returns
    -------
    dict
        a pandas DataFrame containing source data
    """
    # create a dictionary of numpy Series objects; then pass this to pandas DataFrame constructor
    # transpose DataFrame to get expected record-based orientation
    d = {}
    for i, row in enumerate(source_list):
        d[i] = pd.Series(row)

    return pd.DataFrame(d).T

def base_layer_maker(location, collection_type, collection_subtype):
    """
    Writes data to base layer CSV files

    Parameters
    -----------
    location: str
        a folder name that can be found in source-data, such as 'american-left-ephemera'
    collection_type: str
        a term specifying the type of collection for which data will be processed
        (controlled vocabulary: 'archival', 'serial', or 'monograph')
    collection_subtype: str
        a term specifying the subtype of collection for which data will be processed
        (controlled vocabulary: 'catalog', 'digital', or 'physical')

    Returns
    -------
    dict
        a pandas DataFrame containing source data
    """
    
    # validate arguments
    if not os.path.exists('../source-data/%s' % location):
        raise Exception ("location source-data/%s not found!" % (location,))

    if collection_type not in ['archival', 'monograph', 'serial']:
        raise Exception ("collection type '%s' not one of 'archival', 'monograph', or 'serial'." % (collection_type,))

    if collection_subtype not in ['catalog', 'digital', 'physical']:
        raise Exception ("collection subtype '%s' not one of 'catalog', 'digital', or 'physical'." % (collection_subtype,))

    if collection_type == 'archival' and collection_subtype == 'catalog':
        raise Exception ("collection subtype '%s' can only be used with collection type 'monograph' or 'serial'." % (collection_subtype,))

    if collection_type != 'archival' and collection_subtype == 'physical':
        raise Exception ("collection subtype '%s' can only be used with collection type 'archival'." % (collection_subtype,))

    # route source data processing based on type
    result = {}
    collection_dir, item_dir = "", ""

    if collection_type == 'archival' or collection_subtype == 'digital':
        collection_dir = "../source-data/%s/ead/" % location
        if not os.path.exists(collection_dir):
            raise Exception ("location %s not found!" % (collection_dir,))

    if collection_type == 'monograph' or collection_type == 'serial' or collection_subtype == 'digital':
        item_dir = "../source-data/%s/mods/" % location
        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))

    [coll_list, item_list] = process_source_data(collection_type, collection_subtype, collection_dir, item_dir)

    # convert output_rows to pandas dataframe and use to_csv()
    # write row to yml or md file

    coll_df = create_data_frame_from_list(coll_list)
    item_df = create_data_frame_from_list(item_list)

    # create subdirectory in base-layers for that location
    newdir = "../base-layers/" + location
    try:
        os.stat(newdir)
    except:
        os.mkdir(newdir)

    coll_csv = open(newdir + "/" + location + "-collection-base-layer.csv", 'w', encoding="utf-8")
    coll_csv.write(coll_df.to_csv())
    coll_csv.close()

    item_csv = open(newdir + "/" + location + "-item-base-layer.csv", 'w', encoding="utf-8")
    item_csv.write(item_df.to_csv())
    item_csv.close()
    print("success!")
    return

def process_source_data(collection_type, collection_subtype, collection_dir, item_dir):
    """
    Writes data to base layer CSV files.

    Parameters
    -----------
    collection_type: str
        a term specifying the type of collection for which data will be processed
        (controlled vocabulary: 'archival', 'serial', or 'monograph')
    collection_subtype: str
        a term specifying the subtype of collection for which data will be processed
        (controlled vocabulary: 'catalog', 'digital', or 'physical')
    collection_dir: str
        a path to a folder containing collection-level source data (EAD) for a collection
    item_dir: str
        a path to a folder containing item-level source data (MODS) for a collection

    Returns
    -------
    collection_output_rows: list
        a list of dictionaries containing collection-level source data (EAD) for a collection;
        can be empty if no data exists
    item_output_rows: list
        a list of dictionaries containing item-level source data (MODS) for a collection;
        can be empty if no data exists
    """

    # collection-level
    collection_data = get_bs_from_xml(collection_dir, 'ead')
    collection_output_rows = []

    if collection_type == 'archival' or collection_subtype == 'digital':
        for x in collection_data:
            row = get_fields_from_bs(x, data_layers_config.EAD_MAP)
            collection_record_dict = {}
            for key in row.keys():
                collection_record_dict[key] = (row[key])
            collection_output_rows.append(collection_record_dict)

    # item-level
    item_data = get_bs_from_xml(item_dir, 'mods')
    item_output_rows = []

    if collection_type == 'monograph' or collection_type == 'serial' or collection_subtype == 'digital':
        if collection_type == 'archival':
            for x in item_data:
                row = get_fields_from_bs(x, data_layers_config.ARCHIVAL_ITEM_MODS_MAP)
                item_record_dict = {}
                for key in row.keys():
                    item_record_dict[key] = row[key]
                item_output_rows.append(item_record_dict)

        else:
            for f in item_data:
                for x in f.find_all('mods'):
                    if collection_type == 'monograph':
                        if collection_subtype == 'catalog':
                            row = get_fields_from_bs(x, data_layers_config.CATALOG_MONOGRAPH_ITEM_MODS_MAP)
                        else:
                            row = get_fields_from_bs(x, data_layers_config.DIGITAL_MONOGRAPH_ITEM_MODS_MAP)
                    elif collection_type == 'serial':
                        if collection_subtype == 'catalog':
                            row = get_fields_from_bs(x, data_layers_config.CATALOG_SERIAL_ITEM_MODS_MAP)
                        else:
                            row = get_fields_from_bs(x, data_layers_config.DIGITAL_SERIAL_ITEM_MODS_MAP)
                    item_record_dict = {}
                    for key in row.keys():
                        item_record_dict[key] = row[key]
                    item_output_rows.append(item_record_dict)

    return collection_output_rows, item_output_rows

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('when running as a script, you must provide three arguments: source collection name, collection type, and collection sub-type')
    base_layer_maker(sys.argv[1], sys.argv[2], sys.argv[3])
