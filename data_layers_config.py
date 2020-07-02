# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
    'finding_aid_identifier': {'bs_exp':'eadid'},
    'finding_aid_title':{'bs_exp':'titleproper'},
    'finding_aid_creator': {'bs_exp':'author'},
    'finding_aid_publisher': {'bs_exp':'publisher'},
    'finding_aid_publication_date': {'bs_exp':'publicationstmt > date'},
    'finding_aid_creation_date': {'bs_exp':'profiledesc > creation > date'},
    'repository':{'bs_exp':'repository > corpname'},
    'acquisition_number':{'bs_exp':'num'},
    'collection_title': {'bs_exp':'archdesc[level=\'collection\'] > did > unittitle'},
    # one or many
    'collection_creator': {'bs_exp':'origination[label=\'creator\'] > *'},
    'collection_language': {'bs_exp':'archdesc[level=\'collection\'] > did > langmaterial > language[langcode]'}, # attribute value
    'collection_extent': {'bs_exp':'physdesc > extent'},
    'collection_temporal_coverage': {'bs_exp':'archdesc[level=\'collection\'] > did > unitdate'},
    # one or many, 1 child per
    'collection_abstract':{'bs_exp':'abstract'},
    # one or many, one p per
    'collection_scope_and_content': {'bs_exp':'archdesc > scopecontent > p'},
    # has em tags, one or many)
    'biography_or_history': {'bs_exp':'bioghist > p'},
    'subject_headings': {'bs_exp':'controlaccess > *'},
    'related_material': {'bs_exp':'relatedmaterial > p'},
    'preferred_citation': {'bs_exp':'prefercite > p'},
    'conditions_governing_use': {'bs_exp':'userestrict > p'}
    # one or many
}

# mappings between base layer fields and BeautifulSoup selectors for MODS

ARCHIVAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':'identifier[type=\"pitt\"]'},
    'title':{'bs_exp':'mods > titleInfo > title'},
    'creator': {'bs_exp':'mods > name'},
    'creation_date': {'bs_exp':'mods > originInfo > dateCreated'}, # also 'mods > originInfo > dateOther'
    'language': {'bs_exp':'language > languageTerm'},
    'type_of_resource': {'bs_exp':'typeOfResource'},
    'genre': {'bs_exp':':not(relatedItem) > genre'},
    'subject': {'bs_exp':'subject > topic'}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':'subject > temporal'},
    'geographic_coverage': {'bs_exp':'subject > geographic'}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'abstract': {'bs_exp':'abstract'},
    'collection_title': {'bs_exp':'relatedItem > titleInfo > title'},
    'series': {'bs_exp':'note[type=\"series\"]'},
    'container': {'bs_exp':'note[type=\"container\"]'},
    'owner': {'bs_exp':'note[type=\"ownership\"]'},
    'depositor': {'bs_exp':'name'} # with role > roleTerm = depositor
}

SERIAL_ITEM_MODS_MAP = {
    'identifier': {'recordInfo > recordIdentifier'},
    'title': {'bs_exp':'titleInfo > title'},
    'uniform_title': {'bs_exp':'titleInfo[type=\"uniform\"] > title'},
    'alternative_title': {'bs_exp':'titleInfo[type=\"alternative\"] > title'},
    'associated_name':{'bs_exp':'name'},
    'publication_place': {'bs_exp':'originInfo > place > placeTerm[type=\"text\"]'},
    'publisher': {'bs_exp':'originInfo > publisher'}, # also 'name > namePart' with role > roleTerm="publisher"
    'start_date': {'bs_exp':'originInfo > dateCreated[point=\"start\"]'}, # also 'originInfo > mods:dateIssued[@point=\"start\"]''
    'end_date': {'bs_exp':'originInfo > dateCreated[point=\"end\"]'}, # also 'originInfo > mods:dateIssued[@point=\"start\"]''
    'edition': {'bs_exp':'originInfo > edition'},
    'issuance': {'bs_exp':'originInfo > issuance'},
    'frequency': {'bs_exp':'originInfo > frequency'},
    'language': {'bs_exp':'language > languageTerm'},
    'type_of_resource': {'bs_exp':'typeOfResource'},
    'format': {'bs_exp':'physicalDescription > form'},
    'extent': {'bs_exp':'physicalDescription > extent'},
    'genre': {'bs_exp':'genre'}, # also 'subject > genre'
    'subject': {'bs_exp':'subject > topic'}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':'subject > temporal'},
    'geographic_coverage': {'bs_exp':'subject > geographic'}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':'targetAudience'},
    'abstract': {'bs_exp':'abstract'},
    'preceded_by': {'bs_exp':'relatedItem[type=\"preceding\"]'},
    'succeeded_by': {'bs_exp':'relatedItem[type=\"succeeding\"]'},
    'issn': {'bs_exp':'identifier[type=\"issn\"]'},
    'lccn': {'bs_exp':'identifier[type=\"lccn\"]'},
    'oclcn': {'bs_exp':'identifier[type=\"oclcn\"]'}
}

DIGITIZED_SERIAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':'identifier[type=\"pitt\"]'},
    'title': {'bs_exp':'titleInfo > title'},
    'uniform_title': {'bs_exp':'titleInfo[type=\"uniform\"] > title'},
    'alternative_title': {'bs_exp':'titleInfo[type=\"alternative\"] > title'},
    'enumeration_chronology': {'bs_exp':'mods > titleInfo > partNumber'},'record_identifier': {'bs_exp':'recordInfo > recordIdentifier'},
    'associated_name':{'bs_exp':'name'},
    'publication_place': {'bs_exp':'originInfo > place > placeTerm[type=\"text\"]'},
    'publisher': {'bs_exp':'originInfo > publisher'}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':'originInfo > dateOther[type=\"sort\"]'},
    'start_date': {'bs_exp':'originInfo > dateCreated[point=\"start\"]'}, # also 'originInfo > mods:dateIssued[@point=\"start\"]''
    'end_date': {'bs_exp':'originInfo > dateCreated[point=\"end\"]'}, # also 'originInfo > mods:dateIssued[@point=\"start\"]''
    'edition': {'bs_exp':'originInfo > edition'},
    'issuance': {'bs_exp':'originInfo > issuance'},
    'frequency': {'bs_exp':'originInfo > frequency'},
    'language': {'bs_exp':'language > languageTerm'},
    'type_of_resource': {'bs_exp':'typeOfResource'},
    'format': {'bs_exp':'physicalDescription > form'},
    'extent': {'bs_exp':'physicalDescription > extent'},
    'genre': {'bs_exp':'genre'}, # also 'subject > genre'
    'subject': {'bs_exp':'subject > topic'}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':'subject > temporal'},
    'geographic_coverage': {'bs_exp':'subject > geographic'}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':'targetAudience'},
    'abstract': {'bs_exp':'abstract'},
    'preceded_by': {'bs_exp':'relatedItem[type=\"preceding\"]'},
    'succeeded_by': {'bs_exp':'relatedItem[type=\"succeeding\"]'},
    'copyright_status': {'bs_exp':'accessCondition > copyright[@copyright.status]'}, #value of copyright.status attribute
    'copyright_holder': {'bs_exp':'accessCondition > copyright > * > name' },
    'copyright_note': {'bs_exp':'accessCondition > copyright > * > note'},
    'record_identifier': {'bs_exp':'recordInfo > recordIdentifier'},
    'issn': {'bs_exp':'identifier[type=\"issn\"]'},
    'lccn': {'bs_exp':'identifier[type=\"lccn\"]'},
    'oclcn': {'bs_exp':'identifier[type=\"oclcn\"]'},
    'depositor': {'bs_exp':'name'}
}

MONOGRAPH_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':'recordIdentifier'},
    'title': {'bs_exp':'titleInfo > title'},
    'uniform_title': {'bs_exp':'titleInfo[type=\"uniform\"] > title'},
    'alternative_title': {'bs_exp':'titleInfo[type=\"alternative\"] > title'},
    'creator': {'bs_exp':'name > namepart'},
    'contributor': {'bs_exp':'name > namepart'},
    'publication_place': {'bs_exp':'originInfo > place > placeTerm[type=\"text\"] '},
    'publisher': {'bs_exp':'originInfo > publisher'},
    'publication_date': {'bs_exp':'originInfo > dateIssued'},
    'creation_date': {'bs_exp':'originInfo'},
    'copyright_date': {'bs_exp':'originInfo > copyrightDate'},
    'edition': {'bs_exp':'originInfo > edition'},
    'issuance': {'bs_exp':'originInfo > issuance'},
    'frequency': {'bs_exp':'originInfo > frequency'},
    'language': {'bs_exp':'language > languageTerm'},
    'type_of_resource': {'bs_exp':'typeOfResource'},
    'form': {'bs_exp':'physicalDescription > form'},
    'extent': {'bs_exp':'physicalDescription > extent'},
    'genre': {'bs_exp':'genre'},
    'subject': {'bs_exp':'subject'},
    'target_audience': {'bs_exp':'targetAudience'},
    'abstract': {'bs_exp':'abstract'},
    'preceded_by': {'bs_exp':'relatedItem[@type=\"preceding\"]''},
    'succeeded_by': {'bs_exp':'relatedItem[@type=\"succeeding\"]'},
    'url': {'bs_exp':'location > url'},
    'lccn': {'bs_exp':'identifier[@type=\"lccn\"]'},
    'oclccn': {'bs_exp':'identifier[@type=\"oclc\"]'}
}

# Feminist underground press records have no dateOther, only dateIssued, point=start and point=end
# No creator either
