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
    # abstract?
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

ARCHIVAL_ITEM_MODS_MAP = {
    'title':{'bs_exp':'mods\:mods > mods\:titleInfo > mods\:title'},
    'identifier': {'bs_exp':'mods\:identifier[type=\"pitt\"]'},
    'creator': {'bs_exp':'mods\:name'},
    'date': {'bs_exp':'mods\:originInfo > mods\:dateCreated'},
    'depositor': {'bs_exp':'mods\:name'},
    'box': {'bs_exp':'mods\:note[type=\"container\"]'},
    'folder': {'bs_exp':'mods\:note[type=\"container\"]'},
    'type_of_resource': {'bs_exp':'mods\:typeOfResource'},
    'genre': {'bs_exp':'mods\:genre'}
}

SERIAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':'mods\:identifier[type=\"pitt\"]'},
    'publication_date': {'bs_exp':'mods\:originInfo > mods\:dateOther[type=\"sort\"]'},
    'enumeration_chronology': {'bs_exp':'mods\:mods > mods\:titleInfo > mods\:partNumber'},'bib_id': {'bs_exp':'mods\:recordInfo > mods\:recordIdentifier'},
    'alternative_title': {'bs_exp':'mods\:titleInfo[type=\"alternative\"] > mods\:title'},
    'author': {'bs_exp':'mods\:name'},
    'contributor': {'bs_exp':'mods\:name'},
    'publisher': {'bs_exp':'mods\:relatedItem > mods\:originInfo > mods\:publisher'},
    'place_of_publication': {'bs_exp':'mods\:relatedItem > mods\:originInfo > mods\:place > mods\:placeTerm[type=\"text\"]'},
    'start_date': {'bs_exp':'mods\:originInfo > mods\:dateCreated[point=\"start\"]'},
    'frequency': {'bs_exp':'mods\:relatedItem > mods\:originInfo > mods\:frequency'},
    'language': {'bs_exp':'mods\:relatedItem > mods\:language > mods\:languageTerm'},
    'genre': {'bs_exp':'mods\:genre'},
    'lc_subject_heading(s)': {'bs_exp':'mods\:subject'},
    #'former_title': {'bs_exp':'mods\:'}, In MARCXML, not MODS
    #'succeeding_title': {'bs_exp':'mods\:'}, In MARCXML, not MODS
    #'library_has': {'bs_exp':'mods\:'}, Not sure where this is found?
    'copyright': {'bs_exp':'mods\:accessCondition'},
    'issn': {'bs_exp':'mods\:identifier[type=\"issn\"]'},
    'lccn': {'bs_exp':'mods\:identifier[type=\"lccn\"]'},
    'oclcn': {'bs_exp':'mods\:identifier[type=\"oclcn\"]'},
}
