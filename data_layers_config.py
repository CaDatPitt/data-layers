# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
    'finding_aid_id': {'bs_exp':['eadid',]},
    'finding_aid_title':{'bs_exp':['titleproper',]},
    'finding_aid_creator': {'bs_exp':['author',]},
    'finding_aid_creation_date': {'bs_exp':['profiledesc > creation > date',]},
    'finding_aid_publisher': {'bs_exp':['publisher',]},
    'finding_aid_publication_date': {'bs_exp':['publicationstmt > date',]},
    'acquisition_number':{'bs_exp':['num',]},
    'collection_title': {'bs_exp':['archdesc[level=\'collection\'] > did > unittitle',]},
    # one or many
    'collection_creator': {'bs_exp':['origination[label=\'creator\'] > *',]},
    'collection_language': {'bs_exp':['archdesc[level=\'collection\'] > did > langmaterial > language[langcode]',]}, # attribute value
    'collection_extent': {'bs_exp':['physdesc > extent',]},
    'collection_temporal_coverage': {'bs_exp':['archdesc[level=\'collection\'] > did > unitdate',]},
    # one or many, one p per
    'collection_scope_and_content': {'bs_exp':['archdesc > scopecontent > p',]},
    # has em tags, one or many)
    'biography_or_history': {'bs_exp':['bioghist > p',]},
    # one or many, 1 child per
    'collection_abstract':{'bs_exp':['abstract',]},
    'subject_headings': {'bs_exp':['controlaccess > *',]},
    'related_material': {'bs_exp':['relatedmaterial > p',]},
    'repository':{'bs_exp':['repository > corpname',]},
    'preferred_citation': {'bs_exp':['prefercite > p',]},
    # one or many
    'conditions_governing_use': {'bs_exp':['userestrict > p',]}
}

# mappings between base layer fields and BeautifulSoup selectors for MODS

ARCHIVAL_ITEM_MODS_MAP = {
    'id': {'bs_exp':['identifier[type=\"pitt\"]',]},
    'title':{'bs_exp':['mods > titleInfo > title',]},  # should also include subTitle and nonSort, formatted as follows: [title]: [subTitle], [nonSort]
    'creator': {'bs_exp':['mods > name',]}, #  with role > roleTerm="creator"
    'contributor': {'bs_exp':['mods > name',]}, #  with role > roleTerm="contributor"
    'creation_date': {'bs_exp':['mods > originInfo > dateCreator',]}, # if contains attribute "point", concatenate values for elements with point="start" and point="end" with a forward slash (/)
    'sort_date': {'bs_exp':['mods > originInfo > dateOther[type=\"sort\"]',]},
    'display_date': {'bs_exp':['mods > originInfo > dateOther[type=\"display\"]',]},
    'language': {'bs_exp':['language > languageTerm',]},
    'type_of_resource': {'bs_exp':['typeOfResource',]},
    'format': {'bs_exp':['physicalDescription > form',]},
    'extent': {'bs_exp':['physicalDescription > extent',]},
    'genre': {'bs_exp':['relatedItem > genre', ]}, # without parent of relatedItem, also 'subject > genre', maybe like roleTerm
    'abstract': {'bs_exp':['abstract',]},
    'subject': {'bs_exp':['subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo']}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':['subject > temporal',]},
    'geographic_coverage': {'bs_exp':['subject > geographic',]}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'host': {'bs_exp':['relatedItem[type=\"host\"] > titleInfo > title',]},
    'series': {'bs_exp':['relatedItem[type=\"host\"] > note[type=\"series\"]',]},
    'container': {'bs_exp':['relatedItem[type=\"host\"] > note[type=\"container\"]',]},
    'owner': {'bs_exp':['relatedItem[type=\"host\"] > note[type=\"ownership\"]',]},
    'depositor': {'bs_exp':['name',]} # with role > roleTerm="depositor"
}

SERIAL_ITEM_MODS_MAP = {
    'id': {'bs_exp':['recordInfo > recordIdentifier',]},
    'title': {'bs_exp':['titleInfo > title',]},
    # should also include subTitle and nonSort, formatted as follows: [title]: [subTitle], [nonSort]
    # If value of subTitle is parenthetical, it should be formatted as following (less the nonSort where if it does not exist): [title] [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['titleInfo[type=\"alternative\"] > title',]},
    'enumeration_chronology': {'bs_exp':['mods > titleInfo > partNumber',]},
    'associated_name':{'bs_exp':['name',]},
    'publication_place': {'bs_exp':['originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['originInfo > publisher',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['originInfo > dateIssued',]}, #
    'start_date': {'bs_exp':['originInfo > dateIssued[point=\"start\"]',]},
    'end_date': {'bs_exp':['originInfo > dateIssued[point=\"end\"]',]}, 
    'edition': {'bs_exp':['originInfo > edition',]},
    'issuance': {'bs_exp':['originInfo > issuance',]},
    'frequency': {'bs_exp':['originInfo > frequency',]},
    'language': {'bs_exp':['language > languageTerm',]},
    'type_of_resource': {'bs_exp':['typeOfResource',]},
    'format': {'bs_exp':['physicalDescription > form',]},
    'extent': {'bs_exp':['physicalDescription > extent',]},
    'genre': {'bs_exp':['genre',]}, # also 'subject > genre'
    'abstract': {'bs_exp':['abstract',]},
    'subject': {'bs_exp':['subject > topic',]}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':['subject > temporal',]},
    'geographic_coverage': {'bs_exp':['subject > geographic',]}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':['targetAudience',]},
    'preceded_by': {'bs_exp':['relatedItem[type=\"preceding\"]',]},
    'succeeded_by': {'bs_exp':['relatedItem[type=\"succeeding\"]',]},
    'issn': {'bs_exp':['identifier[type=\"issn\"]',]},
    'lccn': {'bs_exp':['identifier[type=\"lccn\"]',]},
    'oclcn': {'bs_exp':['identifier[type=\"oclcn\"]']}
}

DIGITIZED_SERIAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':['identifier[type=\"pitt\"]',]},
    'title': {'bs_exp':['titleInfo > title',]},
    # should also include subTitle and nonSort, formatted as follows: [title]: [subTitle], [nonSort]
    # If value of subTitle is parenthetical, it should be formatted as following (less the nonSort where if it does not exist): [title] [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['titleInfo[type=\"alternative\"] > title',]},
    'enumeration_chronology': {'bs_exp':['mods > titleInfo > partNumber',]},
    'associated_name':{'bs_exp':['name',]}, #when not mods:role/mods:roleTerm="depositor"
    'publication_place': {'bs_exp':['originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['originInfo > publisher',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['originInfo > dateOther[type=\"sort\"]',]},
    'start_date': {'bs_exp':['originInfo > dateCreated[point=\"start\"]',]}, # also 'originInfo > mods:dateIssued[@point=\"start\"]'' (?)
    'end_date': {'bs_exp':['originInfo > dateCreated[point=\"end\"]',]}, # also 'originInfo > mods:dateIssued[@point=\"start\"]'' (?)
    'edition': {'bs_exp':['originInfo > edition',]},
    'issuance': {'bs_exp':['originInfo > issuance',]},
    'frequency': {'bs_exp':['originInfo > frequency',]},
    'language': {'bs_exp':['language > languageTerm',]},
    'type_of_resource': {'bs_exp':['typeOfResource',]},
    'format': {'bs_exp':['physicalDescription > form',]},
    'extent': {'bs_exp':['physicalDescription > extent',]},
    'genre': {'bs_exp':['genre',]}, # also 'subject > genre',
    'abstract': {'bs_exp':['abstract',]},
    'subject': {'bs_exp':['subject > topic',]}, # also 'subject > name', 'subject > occupation', 'subject > titleInfo'
    'temporal_coverage': {'bs_exp':['subject > temporal',]},
    'geographic_coverage': {'bs_exp':['subject > geographic',]}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':['targetAudience',]},
    'preceded_by': {'bs_exp':['relatedItem[type=\"preceding\"]',]},
    'succeeded_by': {'bs_exp':['relatedItem[type=\"succeeding\"]',]},
    'copyright_status': {'bs_exp':['accessCondition > copyright[@copyright.status]',]}, # attribute value
    'copyright_holder': {'bs_exp':['accessCondition > copyright > * > name',]},
    'copyright_note': {'bs_exp':['accessCondition > copyright > * > note',]},
    'issn': {'bs_exp':['identifier[type=\"issn\"]',]},
    'lccn': {'bs_exp':['identifier[type=\"lccn\"]',]},
    'oclcn': {'bs_exp':['identifier[type=\"oclcn\"]',]},
    'depositor': {'bs_exp':['name',]} # with role > roleTerm="depositor"
}

MONOGRAPH_ITEM_MODS_MAP = {
    'id': {'bs_exp':['recordIdentifier',]},
    'title': {'bs_exp':['titleInfo > title',]}, # should also include subTitle and nonSort, formatted as follows: [title]: [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['titleInfo[type=\"alternative\"] > title',]},
    'creator': {'bs_exp':['name > namepart',]},
    'contributor': {'bs_exp':['name > namepart',]},
    'publication_place': {'bs_exp':['originInfo > place > placeTerm[type=\"text\"] ',]},
    'publisher': {'bs_exp':['originInfo > publisher',]},
    'publication_date': {'bs_exp':['originInfo > dateIssued',]}, # without attributes
    'encoded_date': {'bs_exp':['originInfo > dateIssued',]}, # with encoding attribute; if contains attribute point="start" and point="end", group the values and split with a forward slash (/).
    'creation_date': {'bs_exp':['originInfo > dateCreated',]}, # also originInfo > dateOther
    'copyright_date': {'bs_exp':['originInfo > copyrightDate',]},
    'edition': {'bs_exp':['originInfo > edition',]},
    'issuance': {'bs_exp':['originInfo > issuance',]},
    'frequency': {'bs_exp':['originInfo > frequency',]},
    'language': {'bs_exp':['language > languageTerm',]},
    'type_of_resource': {'bs_exp':['typeOfResource',]},
    'format': {'bs_exp':['physicalDescription > form',]},
    'extent': {'bs_exp':['physicalDescription > extent',]},
    'genre': {'bs_exp':['genre',]},
    'abstract': {'bs_exp':['abstract',]},
    'subject': {'bs_exp':['subject',]},
    'temporal_coverage': {'bs_exp':['subject > temporal',]},
    'geographic_coverage': {'bs_exp':['subject > geographic',]}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':['targetAudience',]},
    'isbn': {'bs_exp':['identifier[type=\"isbn\"]',]},
    'lccn': {'bs_exp':['identifier[type=\"lccn\"]',]},
    'oclccn': {'bs_exp':['identifier[type=\"oclc\"]',]},
    'url': {'bs_exp':['location > url',]}
}

DIGITIZED_MONOGRAPH_ITEM_MODS_MAP = {
    'id': {'bs_exp':['recordIdentifier',]},
    'title': {'bs_exp':['titleInfo > title',]}, # should also include subTitle and nonSort, formatted as follows: [title]: [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['titleInfo[type=\"alternative\"] > title',]},
    'creator': {'bs_exp':['name > namepart',]},
    'contributor': {'bs_exp':['name > namepart',]},
    'publication_place': {'bs_exp':['originInfo > place > placeTerm[type=\"text\"] ',]},
    'publisher': {'bs_exp':['originInfo > publisher',]},
    'publication_date': {'bs_exp':['originInfo > dateIssued',]}, # without attributes
    'encoded_date': {'bs_exp':['originInfo > dateIssued',]}, # with encoding attribute; if has attribute @point="start" and point="end", group the values and split with a forward slash (/).
    'creation_date': {'bs_exp':['originInfo > dateCreated',]}, # also originInfo > dateOther
    'copyright_date': {'bs_exp':['originInfo > copyrightDate',]},
    'edition': {'bs_exp':['originInfo > edition',]},
    'issuance': {'bs_exp':['originInfo > issuance',]},
    'frequency': {'bs_exp':['originInfo > frequency',]},
    'language': {'bs_exp':['language > languageTerm',]},
    'type_of_resource': {'bs_exp':['typeOfResource',]},
    'format': {'bs_exp':['physicalDescription > form',]},
    'extent': {'bs_exp':['physicalDescription > extent',]},
    'genre': {'bs_exp':['genre',]},
    'abstract': {'bs_exp':['abstract',]},
    'subject': {'bs_exp':['subject',]},
    'temporal_coverage': {'bs_exp':['subject > temporal',]},
    'geographic_coverage': {'bs_exp':['subject > geographic',]}, # also 'subject > hierarchicalGeographic', 'subject > cartographics', 'subject > geographicCoordinates'
    'target_audience': {'bs_exp':['targetAudience',]},
    'isbn': {'bs_exp':['identifier[type=\"isbn\"]',]},
    'lccn': {'bs_exp':['identifier[type=\"lccn\"]',]},
    'oclccn': {'bs_exp':['identifier[type=\"oclc\"]',]},
    'url': {'bs_exp':['location > url',]},
    'depositor': {'bs_exp':['name',]} # with role > roleTerm="depositor"
}

# mappings between base layer fields and BeautifulSoup selectors for RELS-EXT

DIGITAL_ITEM_RDF_MAP = {
      'collection_id': {'bs_exp':['Description > isMemberOfCollection[@rdf:resource]',]}  
}

# Feminist underground press records have no dateOther, only dateIssued, point=start and point=end
# No creator either
