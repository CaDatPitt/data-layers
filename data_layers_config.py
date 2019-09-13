# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
    'identifier': {'bs_exp':'eadid'},
    'finding_aid_title':{'bs_exp':'titleproper'},
    'acquisition_number':{'bs_exp':'num'},
    'finding_aid_creator': {'bs_exp':'author'},
    'repository':{'bs_exp':'repository > corpname'},
    'publisher': {'bs_exp':'publisher'},
    'date_of_publication':{'bs_exp':'publicationstmt>date'},
    'date_of_creation': {'bs_exp':'profiledesc > creation > date'},
    'collection_title': {'bs_exp':'archdesc[\'level\'=\'collection\'] > did > unittitle'},
    # one or many
    'extent': {'bs_exp':'physdesc > extent'},
    'temporal_coverage': {'bs_exp':'archdesc[\'level\'=\'collection\'] > did > unitdate'},
    # one or many, 1 child per
    'collection_creator': {'bs_exp':'origination[\'label\'=\'creator\'] > *'},
    'conditions_governing_use': {'bs_exp':'userestrict > p'},
    # one or many, one p per
    'related material': {'bs_exp':'relatedmaterial > p'},
    # one or many
    'collection_scope_and_content': {'bs_exp':'archdesc > scopecontent > p'},
    # has em tags, one or many)
    'biography_or_history': {'bs_exp':'bioghist > p'},
    'preferred_citation': {'bs_exp':'prefercite > p'},
    'subject_headings': {'bs_exp':'controlaccess > *'},
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