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
}

# mappings between base layer fields and BeautifulSoup selectors for MODS
MODS_MAP = {
    'title':{'bs_exp':'mods\:mods > mods\:titleInfo > mods\:title'},
    'identifier': {'bs_exp':'mods\:identifier[type=\"pitt\"]'},
    'creator': {'bs_exp':'mods\:name', 'helper_funct': 'get_name_by_type', 'args':{'role':'creator'}, 'root_param':'bs' }, 
    'date': {'bs_exp':'mods\:originInfo > mods\:dateCreated'},
    'depositor': {'bs_exp':'mods\:name', 'helper_funct': 'get_name_by_type', 'args':{'role':'depositor'}, 'root_param':'bs' }, 
    'box': {'bs_exp':'mods\:note[type=\"container\"]', 'helper_funct': 'parse_container', 'args':{'container_type':'box'}, 'root_param':'text'},
    'folder': {'bs_exp':'mods\:note[type=\"container\"]', 'helper_funct': 'parse_container', 'args':{'container_type':'folder'}, 'root_param':'text'}, 
    'type_of_resource': {'bs_exp':'mods\:typeOfResource'},
    'genre': {'bs_exp':'mods\:genre'}
}
# will need additional filtering, role=creator, what function to call
# will need additional filtering, role-depositor, what function to call