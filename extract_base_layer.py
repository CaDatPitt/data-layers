from bs4 import BeautifulSoup
import glob, os
from pymarc import MARCReader, record_to_xml

EAD_COLLECTION_FIELDS = {
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

MODS_ITEM_FIELDS = {
    'title':'mods:title',
    'identifier': ['mods:identifier', {'type':'pitt'}]
}


def get_fields_from_bs(bs_object, field_dict):
    """
    This function takes a dictionary of fields, with bs.find arguments as values,
    and/or findall, and returns a dictionary of those fields
    """
    row = {}
    for u in field_dict.keys():
        try:
            field_data = bs_object.select(field_dict[u])
            field_data = [e.text for e in field_data]
        except:
            #respond if it errors or is empty
            field_data = ''
        #parse field if needed ... with conditionals
        row[u] = field_data
    return row

def get_bs_from_xml(_dir, source_type):
    """File types can be ead, mods, or marc binary, returns a list of bs_objects"""
    if source_type == 'marc':
        filenames = glob.glob(_dir+'*.mrc')
    if source_type == 'mods' or source_type == 'ead':
        filenames = glob.glob(_dir+'*.xml')

    bs_objects = []
    for z in filenames:
        if source_type == 'marc':
            with open(z, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    xml = record_to_xml(record).decode("utf-8")

        if source_type == 'mods' or source_type == 'ead':
            with open(z) as f:
                xml = f.read()
        bs = BeautifulSoup(xml, "lxml")
        bs_objects.append(bs)
        return bs_objects

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

    #create subdirectory in base-layers for that location
    newdir = "base-layers/" + location
    try:
        os.stat(newdir)
    except:
        os.mkdir(newdir)

    # route source data processing based on type
    result = {}
    if collection_type == 'archive':
        collection_dir = "source-data/%s/ead/" % location
        if not os.path.exists(collection_dir):
            raise Exception ("location %s not found!" % (collection_dir,))
        item_dir = "source-data/%s/mods/" % location
        if not os.path.exists(item_dir):
            raise Exception ("location %s not found!" % (item_dir,))        
        result = process_archive_source_data(collection_dir, item_dir)

    elif collection_type == 'serial':
        result = process_archive_source_data(location)

    elif collection_type == 'monograph':
        result = process_monograph_source_data(location)

    #convert output_rows to pandas dataframe and use to_csv()
    #write row to yml file

    return result

def process_archive_source_data(collection_dir, item_dir):

    collection_data = get_bs_from_xml(collection_dir, 'ead')
    collection_output_rows = {}
    for x in collection_data:
        row = get_fields_from_bs(x, EAD_COLLECTION_FIELDS)
        for key in row.keys():
            try:
                collection_output_rows[key].append(row[key])
            except:
                collection_output_rows[key] = row[key]

    item_data = get_bs_from_xml(item_dir, 'mods')
    item_output_rows = {}
    for x in item_data:
        row = get_fields_from_bs(x, MODS_ITEM_FIELDS)
        for key in row.keys():
            try:
                item_output_rows[key].append(row[key])
            except:
                item_output_rows[key] = [row[key],]

    return collection_output_rows


def process_serial_source_data(location):
    return

def process_monograph_source_data(location):
    return
