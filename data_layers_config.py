# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
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

# mappings between base layer fields and BeautifulSoup selectors for MODS
MODS_MAP = {
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
