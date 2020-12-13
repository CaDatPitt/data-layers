import argparse
import datetime
import os
import sys
import glob
from bs4 import BeautifulSoup
from pymarc import MARCReader, record_to_xml
import re
import numpy as np
import pandas as pd
import data_layers_config
import encoding_schemes

def base_layer_maker(location, collection_type, collection_subtype, decode=False):
    """
    Parses and extracts data from XML, processes and transforms data into a pandas DataFrame, and writes data to base layer CSV files.

    Parameters
    ----------
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
    None

    Raises
    ------
    Exception: location source-data/[location] not found!
    Exception: location source-data/[directory] not found!
    Exception: collection type '[collection_type]' not one of 'archival', 'monograph', or 'serial'.
    Exception: collection subtype '[collection_subtype]' not one of 'catalog', 'digital', or 'physical'.
    Exception: collection subtype 'catalog' can only be used with collection type 'monograph' or 'serial'.
    Exception: collection subtype 'physical' can only be used with collection type 'archival'.
    """
    # start timer for program execution time
    start_time = datetime.datetime.now()

    # validate arguments
    if not os.path.exists('../source-data/%s' % location):
        raise Exception ("location source-data/%s not found!" % (location,))

    if collection_type not in ['archival', 'monograph', 'serial']:
        raise Exception ("collection type '%s' not one of 'archival', 'monograph', or 'serial'." % (collection_type,))

    if collection_subtype not in ['catalog', 'digital', 'physical']:
        raise Exception ("collection subtype '%s' not one of 'catalog', 'digital', or 'physical'." % (collection_subtype,))

    if collection_type == 'archival' and collection_subtype == 'catalog':
        raise Exception ("collection subtype 'catalog' can only be used with collection type 'monograph' or 'serial'.")

    if collection_type != 'archival' and collection_subtype == 'physical':
        raise Exception ("collection subtype 'physical' can only be used with collection type 'archival'.")

    # route source data processing based on collection type and subtype
    result = {}
    collection_dir, item_dir, relsext_dir = "", "", ""

    if collection_type == 'archival' or collection_subtype == 'digital':
        collection_dir = "../source-data/%s/ead/" % location
        if not os.path.exists(collection_dir):
            raise Exception ("location %s not found!" % (collection_dir,))

        relsext_dir = "../source-data/%s/rels-ext/" % location
        if not os.path.exists(relsext_dir):
            raise Exception ("location %s not found!" % (relsext_dir,))

    if collection_type == 'monograph' or collection_type == 'serial' or collection_subtype == 'digital':
        item_dir = "../source-data/%s/mods/" % location
        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))

    [coll_list, item_list, coll_relsext_list, item_relsext_list] = process_source_data(collection_type, collection_subtype, collection_dir, item_dir, relsext_dir)

    # convert output_rows to pandas DataFrames and use to_csv()
    coll_df = create_data_frame_from_list(coll_list)
    item_df = create_data_frame_from_list(item_list)

    coll_relsext_df = create_data_frame_from_list(coll_relsext_list)
    item_relsext_df = create_data_frame_from_list(item_relsext_list)

    # merge relsext DataFrames with collection and item DataFrames
    if collection_subtype == 'digital':
        if not coll_df.empty and not coll_relsext_df.empty:
            coll_df = (pd.merge(coll_df, coll_relsext_df, how='left', left_on=['finding_aid_id'], right_on=['coll_id'])).drop('coll_id', axis=1)
        if not item_df.empty and not item_relsext_df.empty:
            item_df = (pd.merge(item_df, item_relsext_df, how='left', left_on=['id'], right_on=['item_id'])).drop('item_id', axis=1)

    # decode values in encoded columns
    if decode:
        coll_df = decode_values(coll_df)
        item_df = decode_values(item_df)

    # create subdirectory in base-layers for that location
    newdir = "../base-layers/" + location
    try:
        os.stat(newdir)
    except:
        os.mkdir(newdir)

    # write collection and item DataFrames to CSV
    coll_csv = open(newdir + "/" + location.replace("/", "-").replace(" ", "-") + "_collection-base-layer.csv", 'w', encoding='utf-8', newline='')
    coll_csv.write(coll_df.to_csv(index=False))
    coll_csv.close()

    item_csv = open(newdir + "/" + location.replace("/", "-").replace(" ", "-") + "_item-base-layer_" + collection_type + ".csv", 'w', encoding='utf-8', newline='')
    item_csv.write(item_df.to_csv(index=False) )
    item_csv.close()

    # notify that program has completed successfully
    print("Success!")

    # stop timer, then calculate and display program execution time
    end_time = datetime.datetime.now()
    print("Execution Time: " + str(end_time - start_time))

    return

def process_source_data(collection_type, collection_subtype, collection_dir, item_dir, relsext_dir):
    """
    Parses, extracts, and processes source data.

    Parameters
    ----------
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
    # create rows of data in dictionaries
    # collection level
    collection_data = get_bs_from_xml(collection_dir, 'ead')
    collection_output_rows = []

    if collection_type == 'archival' or collection_subtype == 'digital':
        for x in collection_data:
            row = get_fields_from_bs(x, data_layers_config.EAD_MAP)
            collection_record_dict = {}
            for key in row.keys():
                collection_record_dict[key] = (row[key])
            collection_output_rows.append(collection_record_dict)

    # item level
    item_data = get_bs_from_xml(item_dir, 'mods')
    item_output_rows = []

    if collection_type == 'monograph' or collection_type == 'serial' or collection_subtype == 'digital':
        for f in item_data:
            for x in f.find_all('mods'):
                if collection_type == 'archival':
                    row = get_fields_from_bs(x, data_layers_config.ARCHIVAL_ITEM_MODS_MAP)
                if collection_type == 'monograph':
                    if collection_subtype == 'catalog':
                        row = get_fields_from_bs(x, data_layers_config.CATALOG_MONOGRAPH_ITEM_MODS_MAP)
                    elif collection_subtype == 'digital':
                        row = get_fields_from_bs(x, data_layers_config.DIGITAL_MONOGRAPH_ITEM_MODS_MAP)
                elif collection_type == 'serial':
                    if collection_subtype == 'catalog':
                        row = get_fields_from_bs(x, data_layers_config.CATALOG_SERIAL_ITEM_MODS_MAP)
                    elif collection_subtype == 'digital':
                        row = get_fields_from_bs(x, data_layers_config.DIGITAL_SERIAL_ITEM_MODS_MAP)
                item_record_dict = {}
                for key in row.keys():
                    item_record_dict[key] = row[key]
                item_output_rows.append(item_record_dict)

    # rels-ext (rdf)
    relsext_data = get_bs_from_xml(relsext_dir, 'rdf')
    coll_relsext_output_rows = []
    item_relsext_output_rows = []

    if collection_subtype == 'digital':
        # collection level
        for x in relsext_data:
            row = get_fields_from_bs(x, data_layers_config.DIGITAL_COLLECTION_RDF_MAP)
            collection_relsext_record_dict = {}
            for key in row.keys():
                collection_relsext_record_dict[key] = (row[key])
            coll_relsext_output_rows.append(collection_relsext_record_dict)

        # item level
        for x in relsext_data:
            row = get_fields_from_bs(x, data_layers_config.DIGITAL_ITEM_RDF_MAP)
            item_relsext_record_dict = {}
            for key in row.keys():
                item_relsext_record_dict[key] = (row[key])
            item_relsext_output_rows.append(item_relsext_record_dict)

    return collection_output_rows, item_output_rows, coll_relsext_output_rows, item_relsext_output_rows

def create_data_frame_from_list(source_list):
    """
    Creates a pandas DataFrame from a list of dictionaries.

    Parameters
    ----------
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

def get_bs_from_xml(_dir, source_type):
    """
    Reads source data files and returns list of BeautifulSoup objects.

    Parameters
    ----------
    _dir: str
        the path to a directory
    source_type: str
        the type of a source data file ('mods', 'marc', or 'mods')

    Returns
    -------
    bs_objects: list
         a list of BeautifulSoup objects
    """

    # find and account for relevant files by file type
    if source_type == 'marc':
        filenames = glob.glob(_dir + '*.mrc')
    if source_type == 'mods' or source_type == 'ead' or source_type == 'rdf':
        filenames = glob.glob(_dir + '*.xml')

    print("Working with %d %s files..." % (len(filenames), source_type.upper()))

    bs_objects = []

    # get bs objects from XML files
    for z in filenames:
        # if file type is marc binary, use pymarc to convert to xml
        if source_type == 'marc':
            with open(z, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    xml = record_to_xml(record).decode('utf-8')
                    bs = BeautifulSoup(xml, "xml")
                    bs_objects.append(bs)

        # if file type is mods, ead, rdf, read as xml
        if source_type == 'mods' or source_type == 'ead' or source_type == 'rdf':
            with open(z, encoding='utf-8') as f:
                xml = f.read()
            bs = BeautifulSoup(xml, 'xml')
            bs_objects.append(bs)

    return bs_objects

def get_fields_from_bs(bs_object, field_dict):
    """
    Parses, extracts, and processes data from XML to populate CSV fields.

    Parameters
    ----------
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
    exceptions = ['title', 'associated_name', 'creator', 'contributor', 'depositor',
    'publisher', 'publication_date', 'encoded_date', 'genre', 'type_of_resource',
    'geographic_coverage', 'copyright_status', 'collection_language', 'collection_id',
    'coll_id', 'item_id']

    for key in field_dict.keys():
        # assume that field_dict[key]['bs_exp'] is a list of expressions
        expressions = field_dict[key]['bs_exp']
        field_data = ""

        for exp in expressions:

            # get and process/format element values to generate field data for rows
            if key not in exceptions:
                results = bs_object.select(exp)
                field_list = []

                for result in results:
                    value = result.text.replace("\n", " ").replace("\t", " ").strip()
                    joined_value = " ".join(value.split())
                    if joined_value != "" and omit_repeats(joined_value, field_list):
                        field_list.append(joined_value)
                        field_data += "|||" + joined_value
                field_data = field_data.strip('|||')

            if key == 'title':
                results = bs_object.select(exp)
                field_list = []

                # check titleInfo child element names and get matched element values
                # concatenate child element values with specified punctuation for formatting purposes
                for result in results:
                    title_value, subTitle_value, nonSort_value = "", "", ""
                    for child in result.children:
                        if child.name == 'title':
                            title_value = child.string.strip()
                        if child.name == 'subTitle':
                            if child.string != "" and child.string[0] == "(":
                                subTitle_value = " " + child.string.strip()
                            else:
                                subTitle_value = ": " + child.string.strip()
                        if child.name == 'nonSort':
                            nonSort_value = ", " + child.string.strip()
                    field_list.append(title_value + subTitle_value + nonSort_value)
                field_data += "|||".join(field_list)

            if key == 'associated_name' or key == 'creator' or key == 'contributor' or key == 'depositor':
                results = bs_object.select(exp)
                value = ""
                field_list = []

                # if name element, look for a grandchild and check value, then get text from matched child element(s)
                for result in results:
                    value = get_name_by_grandchild(result, key, 'namePart', 'role > roleTerm')
                    if value != "" and omit_repeats(value, field_list):
                        field_list.append(value)
                field_data += "|||".join(field_list)

            if key == 'publisher':
                results = bs_object.select(exp)
                field_list = []

                # check if publisher data contained in publisher element or name element (the else case)
                # if name element, look for a grandchild and check value, then get text from matched child element(s)
                for result in results:
                    value = ""
                    if result.name == 'publisher':
                        value = result.text.strip()
                    else:
                        value = get_name_by_grandchild(result, key, 'namePart', 'role > roleTerm')
                    joined_value = " ".join(value.split())
                    if joined_value != "":
                        field_data += "|||" + joined_value
                field_data = field_data.strip('|||')

            if key == 'publication_date':
                results = bs_object.select(exp)
                value = ""
                field_list = []

                # check if element has attributes and, if not, get value
                for result in results:
                    if not(result.attrs):
                        value = result.text.strip()
                        joined_value = " ".join(value.split())
                        if joined_value != "" and omit_repeats(joined_value, field_list):
                            field_list.append(joined_value)
                field_data += "|||".join(field_list)

            if key == 'encoded_date':
                results = bs_object.select(exp)
                start_value, end_value, other_value = "", "", ""

                # check if element has point attribute (point="start" or point="end")
                # if so, get start value and end value and, if both exist, concatenate with a forward-slash
                # if not, simply get value
                for result in results:
                    if result.has_attr('point'):
                        if result['point'] == "start":
                            start_value = result.text.strip()
                        elif result['point'] == "end" and end_value == "":
                            end_value += "/" + result.text.strip()
                    if not(result.has_attr('point')):
                       other_value = "|||" + result.text.strip()
                       if other_value != "":
                           field_data += "|||" + other_value
                if start_value != "" or end_value != "":
                    field_data += "|||" + start_value + end_value
                field_data = field_data.strip('|||')

            if key == 'genre' or key == 'type_of_resource':
                results = bs_object.select(exp)
                value = ""
                field_list = []

                # get values, remove trailing punctuation, and sort
                for result in results:
                    value = omit_trailing_punct((result.text).strip())
                    if value != "" and omit_repeats(value, field_list):
                        field_list.append(value)
                field_list.sort()
                field_data += "|||".join(field_list)

            if key == 'geographic_coverage':
                results = bs_object.select(exp)
                field_list = []

                for result in results:
                    if result.name == 'hierarchicalGeographic':
                        hierarchical_field_list = []
                        for child in result.children:
                            child_value = child.string.replace("\n", " ").replace("\t", " ").strip()
                            if child_value != "":
                                hierarchical_field_list.append(child_value)
                        joined_value = ", ".join(hierarchical_field_list)
                    else:
                        value = result.text.replace("\n", " ").replace("\t", " ").strip()
                        joined_value = " ".join(value.split())
                    if joined_value != "" and omit_repeats(joined_value, field_list):
                        field_list.append(joined_value)
                        field_data += "|||" + joined_value
                field_data = field_data.strip('|||')

            # get and process/format element attribute values to generate field data for rows
            if key == 'copyright_status':
                results = bs_object.select(exp)
                for result in results:
                    field_data += results[0]['copyright.status']

            if key == 'collection_language':
                results = bs_object.select(exp)
                for result in results:
                    field_data += results[0]['langcode']

            if key == 'coll_id' or key == 'item_id':
                results = bs_object.select(exp)
                for result in results:
                    value = results[0]['rdf:about']
                    field_data += value.strip("info:fedora/pitt:")

            if key == 'collection_id':
                results = bs_object.select(exp)
                i = 0
                for result in results:
                    value = results[i]['rdf:resource']
                    field_data += "|||" + value.strip("info:fedora/pitt:")
                    field_data = field_data.strip("|||")
                    i += 1

        row[key] = field_data

    return row

def get_name_by_grandchild(bs_object, key, children='namePart', grandchild_exp='role > roleTerm'):
    """
    Extract and processes namePart element values and, in specified cases, roleTerm element values.

    Parameters
    ----------
    bs_object: bs4.BeautifulSoup
        a BeautifulSoup object
    grandchild_exp: str
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
    roleTerm_tags = bs_object.select(grandchild_exp)
    specified_roleTerms = [['author', 'authors', 'aut', 'composer', 'composers', 'cmp',
    'creator', 'creators', 'cre', 'dubious author', 'dub', 'editor', 'editors', 'edt',
    'joint author', 'joint authors', 'screenwriter', 'aus','supposed author', 'supposed authors'],
    ['publisher', 'publishers', 'pbl'], ['depositor']]
    creator, publisher, depositor = specified_roleTerms[0], specified_roleTerms[1], specified_roleTerms[2]
    matched_roleTerm_list = []
    name_parts_joined = ""
    match = False

    # match where roleTerm value is in the appropriate sublist of specified_roleTerms, based on key
    if name_tags.role:
        for tag in roleTerm_tags:
            roleTerm_value = omit_trailing_punct(tag.text.strip())
            if key == 'creator':
                if roleTerm_value in creator:
                    match = True
            elif key == 'depositor':
                if roleTerm_value in depositor:
                    match = True
            elif key == 'publisher':
                if roleTerm_value in publisher:
                    match = True
            elif key == 'associated_name':
                if roleTerm_value not in 'depositor':
                    match = True
                    if roleTerm_value != "":
                        matched_roleTerm_list.append(roleTerm_value)
            elif key == 'contributor':
                if not(any(roleTerm_value in sublist for sublist in specified_roleTerms)):
                    match = True
                    if roleTerm_value != "":
                        matched_roleTerm_list.append(roleTerm_value)

    # match where no role exists
    else:
        if key == 'creator' and bs_object.has_attr('usage'):
            match = True
        elif key == 'contributor' and not(bs_object.has_attr('usage')):
            match = True

    # if name matches key, concatenate all namePart values, separated by a comma
    # if key is 'associated name' or 'contributor', also concatenate roleTerm values in parentheses
    # remove empty parentheses
    if match:
        name_parts_joined += ", ".join([i.text.strip() for i in namePart_tags])
        if key == 'contributor' or key == 'associated_name' and name_tags.role and matched_roleTerm_list:
            matched_roleTerms = ", ".join(matched_roleTerm_list)
            name_parts_joined += " (" + matched_roleTerms + ")"
            if name_parts_joined[-3:] == " ()":
                name_parts_joined = name_parts_joined[0:-3]

    return name_parts_joined

def omit_repeats(value, field_list):
    """
    Checks if a value already exists in a list.

    Parameters
    ----------
    value: str
        processed text from a bs.find result

    Returns
    -------
    boolean
         True if the value is not already in the list; False if it is
    """

    value = value.lower()
    field_list = [i.lower() for i in field_list]
    if value in field_list or omit_trailing_punct(value) in field_list:
        return False
    else:
        return True

def omit_trailing_punct(text):
    """
    Removes specified trailing punctuation from a string.

    Parameters
    ----------
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

def decode_values(df):
    """
    Replaces encoded values in the specified dataset column(s) with the corresponding decoded values.

    Parameters
    ----------
    file_location: str
        a location or absolute path of the file to be used
    column: str
        a column name, as it appears in the file, containing the encoded values to be decoded

    Returns
    -------
    None
    """

    encoded_columns = {
    'collection_language': ['iso639-2b'],
    'language': ['iso639-2b'],
    'geographic_coverage': ['marccountry', 'marcgac']
    }
    encoding_dict = {}

    for column in encoded_columns.keys():
        # build dictionary from appropriate encoding schemes for column
        for encoding_scheme in encoded_columns[column]:
            encoding_dict.update(encoding_schemes.LIST[encoding_scheme])

        # pre-process and decode fields in column and keep count of total and decoded values
        value_count, decoded_value_count = 0, 0
        if column in df.columns:
            for i in df.index:
                field_data = df.at[i, column]
                field_list = []
                decoded_field_list = []
                if isinstance(field_data, str):
                    field_list = (field_data).split('|||')
                    for value in field_list:
                        processed_value = value.strip('-\n\t ').lower()
                        decoded_value = ""
                        if value != "":
                            value_count += 1
                        for code in encoding_dict.keys():
                            if processed_value == code:
                                decoded_value = processed_value.replace(code, encoding_dict[code])
                                decoded_value_count += 1
                                break
                            else:
                                decoded_value = value
                        decoded_field_list.append(decoded_value)
                df.at[i, column] = "|||".join(set(decoded_field_list))

            # report counts of evaluated values and decoded values in column
            print(str(decoded_value_count) + " out of " + str(value_count) + " values decoded in '" + column + "' column.")

    return df

def parse_arguments():
    """
    Parses command line arguments.

    Parameters
    ----------
    None

    Returns
    -------
    args: dict
        dictionary of arguments
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        prog="extract_base_layer",
        description="Parses and extracts data from XML, processes and transforms data into a pandas DataFrame, and writes data to base layer CSV files.",
        epilog="To run the script, your command should be input as follows: python extract_base_layer.py [location] [collection_type] [collection_subtype] (--decode)"
        )
    # Positional mandatory arguments
    parser.add_argument("location", help="a folder name that can be found in the 'source-data' directory", type=str)
    parser.add_argument("collection_type", help="a term specifying the type of collection for which data will be processed (valid options: 'archival', 'serial', 'monograph')", type=str, choices=['archival', 'serial', 'monograph'], metavar='collection_type')
    parser.add_argument("collection_subtype", help="a term specifying the subtype of collection for which data will be processed (valid options: 'catalog,' 'digital')", type=str, choices=['catalog', 'digital'], metavar='collection_subtype')

    # Optional arguments
    parser.add_argument("--decode", help="decode encoded values (default=False)", default=False, action='store_true')

    # Parse arguments
    args = parser.parse_args()

    return args

# call main function
if __name__ == '__main__':
    # parse the arguments
    args = parse_arguments()
    # raw print arguments
    print("You are running the script with the following arguments:")
    for a in args.__dict__:
        print('  * ' + str(a) + ": " + str(args.__dict__[a]))
    # run function
    base_layer_maker(args.location, args.collection_type, args.collection_subtype, args.decode)
