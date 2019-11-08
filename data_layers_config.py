# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
    'identifier': {'bs_exp':'eadid'},
    'finding_aid_title':{'bs_exp':'titleproper'},
    'acquisition_number':{'bs_exp':'num'},
    'finding_aid_creator': {'bs_exp':'author'},
    'repository':{'bs_exp':'repository > corpname'},
    'publisher': {'bs_exp':'publisher'},
    'date_of_publication':{'bs_exp':'publicationstmt > date'},
    'date_of_creation': {'bs_exp':'profiledesc > creation > date'},
    'collection_title': {'bs_exp':'archdesc[level=\'collection\'] > did > unittitle'},
    # one or many
    'extent': {'bs_exp':'physdesc > extent'},
    'temporal_coverage': {'bs_exp':'archdesc[level=\'collection\'] > did > unitdate'},
    # one or many, 1 child per
    # abstract?
    'collection_creator': {'bs_exp':'origination[label=\'creator\'] > *'},
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
    'identifier': {'bs_exp':'identifier[type=\"pitt\"]'},
    'title':{'bs_exp':'mods > titleInfo > title'},
    'creator': {'bs_exp':'mods > name'},
    'date_created': {'bs_exp':'mods > originInfo > dateCreated'},
    'date_issued': {'bs_exp':'mods > originInfo > dateIssued'}, 
    'depositor': {'bs_exp':'mods > name'},
    'box': {'bs_exp':'note[type=\"container\"]'},
    'folder': {'bs_exp':'note[type=\"container\"]'},
    'type_of_resource': {'bs_exp':'typeOfResource'},
    'genre': {'bs_exp':':not(relatedItem) > genre'}
}

SERIAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':'identifier[type=\"pitt\"]'},
    'title': {'bs_exp':'titleInfo > title'},
    'alternative_title': {'bs_exp':'titleInfo[type=\"alternative\"] > title'},
    'depositor': {'bs_exp':'name'},
    'enumeration_chronology': {'bs_exp':'mods > titleInfo > partNumber'},'bib_id': {'bs_exp':'recordInfo > recordIdentifier'},
    #'associated_names':{'bs_exp':'name'},
    'publisher': {'bs_exp':'relatedItem > originInfo > publisher'},
    'place_of_publication': {'bs_exp':'relatedItem > originInfo > place > placeTerm[type=\"text\"]'},
    'publication_date': {'bs_exp':'originInfo > dateOther[type=\"sort\"]'},
    'start_date': {'bs_exp':'originInfo > dateCreated[point=\"start\"]'},
    'end_date': {'bs_exp':'originInfo > dateCreated[point=\"end\"]'},
    'frequency': {'bs_exp':'relatedItem > originInfo > frequency'},
    'language': {'bs_exp':'relatedItem > language > languageTerm'},
    'format': {'bs_exp':'physicalDescription > form'},
    'extent': {'bs_exp':'physicalDescription > extent'},
    'genre': {'bs_exp':'genre'},
    'lc_subject_heading(s)': {'bs_exp':'subject'},
    #'former_title': {'bs_exp':''}, In MARCXML, not MODS
    #'succeeding_title': {'bs_exp':''}, In MARCXML, not MODS
    #'library_has': {'bs_exp':''}, Not sure where this is found?
    'copyright_status': {'bs_exp':'accessCondition > copyright'}, #copyright.status attribute
    'copyright_holder': {'bs_exp':'accessCondition > copyright > * > name' },
    'copyright_note': {'bs_exp':'accessCondition > copyright > * > note'},
    'bibid': {'bs_exp':'recordInfo > recordIdentifier'},
    'issn': {'bs_exp':'identifier[type=\"issn\"]'},
    'lccn': {'bs_exp':'identifier[type=\"lccn\"]'},
    'oclcn': {'bs_exp':'identifier[type=\"oclcn\"]'},
    #'former_title': {'bs_exp':''}, In MARCXML, not MODS
    #'succeeding_title': {'bs_exp':''}, In MARCXML, not MODS
    #'library_has': {'bs_exp':''}, Not sure where this is found?
    'depositor': {'bs_exp':'name'},
}
