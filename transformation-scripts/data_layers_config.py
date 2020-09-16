# mappings between base layer fields and BeautifulSoup selectors for EAD
EAD_MAP = {
    'finding_aid_id': {'bs_exp':['eadid',]},
    'finding_aid_title':{'bs_exp':['titleproper',]},
    'finding_aid_creator': {'bs_exp':['author',]},
    'finding_aid_creation_date': {'bs_exp':['profiledesc > creation > date',]},
    'finding_aid_publisher': {'bs_exp':['publisher',]},
    'finding_aid_pub_date': {'bs_exp':['publicationstmt > date',]},
    'acquisition_number':{'bs_exp':['num',]},
    'collection_title': {'bs_exp':['archdesc[level=\'collection\'] > did > unittitle',]},
    # one or many
    'collection_creator': {'bs_exp':['origination[label=\'creator\'] > *',]},
    'collection_language': {'bs_exp':['archdesc[level=\'collection\'] > did > langmaterial > language[langcode]',]}, # attribute value
    'collection_extent': {'bs_exp':['physdesc > extent',]},
    'collection_temp_coverage': {'bs_exp':['archdesc[level=\'collection\'] > did > unitdate',]},
    # one or many, one p per
    'collection_scope_content': {'bs_exp':['archdesc > scopecontent > p',]},
    # has em tags, one or many)
    'biography_history': {'bs_exp':['bioghist > p',]},
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
    'id': {'bs_exp':['mods > identifier[type=\"pitt\"]',]},
    'title':{'bs_exp':['mods > titleInfo:not([type]) > title', 'mods > titleInfo > subTitle', 'mods > titleInfo > nonSort',]},  # formatted as follows: [title]: [subTitle], [nonSort]
    'creator': {'bs_exp':['mods > name',]},
    'contributor': {'bs_exp':['mods > name',]},
    'creation_date': {'bs_exp':['mods > originInfo > dateCreated',]},
    'sort_date': {'bs_exp':['mods > originInfo > dateOther[type=\"sort\"]',]},
    'display_date': {'bs_exp':['mods > originInfo > dateOther[type=\"display\"]',]},
    'language': {'bs_exp':['mods > language > languageTerm',]},
    'type_of_resource': {'bs_exp':['mods > typeOfResource',]},
    'format': {'bs_exp':['mods > physicalDescription > form',]},
    'extent': {'bs_exp':['mods > physicalDescription > extent',]},
    'genre': {'bs_exp':['*:not(relatedItem) > genre', ]}, # without parent of relatedItem; includes 'subject > genre'
    'abstract': {'bs_exp':['mods > abstract',]},
    'subject': {'bs_exp':['mods > subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo']},
    'temporal_coverage': {'bs_exp':['mods > subject > temporal',]},
    'geographic_coverage': {'bs_exp':['mods > geographic', 'hierarchicalGeographic', 'cartographics', 'geographicCoordinates']},
    'host': {'bs_exp':['mods > relatedItem[type=\"host\"] > titleInfo > title',]},
    'series': {'bs_exp':['mods > relatedItem[type=\"host\"] > note[type=\"series\"]',]},
    'container': {'bs_exp':['mods > relatedItem[type=\"host\"] > note[type=\"container\"]',]},
    'owner': {'bs_exp':['mods > relatedItem[type=\"host\"] > note[type=\"ownership\"]',]},
    'depositor': {'bs_exp':['mods > name',]}
}

CATALOG_SERIAL_ITEM_MODS_MAP = {
    'id': {'bs_exp':['mods > recordInfo > recordIdentifier',]},
    'title':{'bs_exp':['mods > titleInfo:not([type]) > title', 'mods > titleInfo > subTitle', 'mods > titleInfo > nonSort',]},
    # Formatted as follows: [title]: [subTitle], [nonSort]
    # If value of subTitle is parenthetical, it should be formatted as following (less the nonSort where if it does not exist): [title] [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['mods> titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['mods > titleInfo[type=\"alternative\"] > title',]},
    'enumeration_chronology': {'bs_exp':['mods > titleInfo > partNumber',]},
    'associated_name':{'bs_exp':['mods > name',]},
    'publication_place': {'bs_exp':['mods > originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['mods > originInfo > publisher', 'mods > name',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['mods > originInfo > dateIssued',]},
    'start_date': {'bs_exp':['mods > originInfo > dateIssued[point=\"start\"]',]},
    'end_date': {'bs_exp':['mods > originInfo > dateIssued[point=\"end\"]',]},
    'edition': {'bs_exp':['mods > originInfo > edition',]},
    'issuance': {'bs_exp':['mods > originInfo > issuance',]},
    'frequency': {'bs_exp':['mods > originInfo > frequency',]},
    'language': {'bs_exp':['mods > language > languageTerm',]},
    'type_of_resource': {'bs_exp':['mods > typeOfResource',]},
    'format': {'bs_exp':['mods > physicalDescription > form',]},
    'extent': {'bs_exp':['mods > physicalDescription > extent',]},
    'genre': {'bs_exp':['*:not(relatedItem) > genre', ]}, # without parent of relatedItem; includes 'subject > genre'
    'abstract': {'bs_exp':['mods > abstract',]},
    'subject': {'bs_exp':['mods > subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo']},
    'temporal_coverage': {'bs_exp':['mods > subject > temporal',]},
    'geographic_coverage': {'bs_exp':['mods > geographic', 'hierarchicalGeographic', 'cartographics', 'geographicCoordinates',]},
    'target_audience': {'bs_exp':['mods > targetAudience',]},
    'preceded_by': {'bs_exp':['mods > relatedItem[type=\"preceding\"]',]},
    'succeeded_by': {'bs_exp':['mods > relatedItem[type=\"succeeding\"]',]},
    'issn': {'bs_exp':['mods > identifier[type=\"issn\"]',]},
    'lccn': {'bs_exp':['mods > identifier[type=\"lccn\"]',]},
    'oclcn': {'bs_exp':['mods > identifier[type=\"oclcn\"]']}
}

DIGITAL_SERIAL_ITEM_MODS_MAP = {
    'identifier': {'bs_exp':['mods > identifier[type=\"pitt\"]',]},
    'title':{'bs_exp':['mods > titleInfo:not([type]) > title', 'mods > titleInfo > subTitle', 'mods > titleInfo > nonSort',]},
    # Formatted as follows: [title]: [subTitle], [nonSort]
    # If value of subTitle is parenthetical, it should be formatted as following (less the nonSort where if it does not exist): [title] [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['mods > titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['mods > titleInfo[type=\"alternative\"] > title',]},
    'enumeration_chronology': {'bs_exp':['mods > titleInfo > partNumber',]},
    'associated_name':{'bs_exp':['name',]}, # when not mods:role/mods:roleTerm="depositor"
    'publication_place': {'bs_exp':['mods > originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['mods > originInfo > publisher', 'mods > name',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['mods > originInfo > dateOther[type=\"sort\"]',]},
    'start_date': {'bs_exp':['mods > originInfo > dateCreated[point=\"start\"]', 'mods > originInfo > dateIssued[point=\"start\"]',]},
    'end_date': {'bs_exp':['mods > originInfo > dateCreated[point=\"end\"]', 'mods > originInfo > dateIssued[point=\"end\"]',]},
    'edition': {'bs_exp':['mods > originInfo > edition',]},
    'issuance': {'bs_exp':['mods > originInfo > issuance',]},
    'frequency': {'bs_exp':['mods > originInfo > frequency',]},
    'language': {'bs_exp':['mods > language > languageTerm',]},
    'type_of_resource': {'bs_exp':['mods > typeOfResource',]},
    'format': {'bs_exp':['mods > physicalDescription > form',]},
    'extent': {'bs_exp':['mods > physicalDescription > extent',]},
    'genre': {'bs_exp':['*:not(relatedItem) > genre', ]}, # without parent of relatedItem; includes 'subject > genre'
    'abstract': {'bs_exp':['mods > abstract',]},
    'subject': {'bs_exp':['mods > subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo',]},
    'temporal_coverage': {'bs_exp':['mods > subject > temporal',]},
    'geographic_coverage': {'bs_exp':['mods > geographic', 'hierarchicalGeographic', 'cartographics', 'geographicCoordinates',]},
    'target_audience': {'bs_exp':['mods > targetAudience',]},
    'preceded_by': {'bs_exp':['mods > relatedItem[type=\"preceding\"]',]},
    'succeeded_by': {'bs_exp':['mods > relatedItem[type=\"succeeding\"]',]},
    'copyright_status': {'bs_exp':['accessCondition > copyright',]}, # attribute value
    'copyright_holder': {'bs_exp':['accessCondition > copyright > * > name',]},
    'copyright_note': {'bs_exp':['accessCondition > copyright > * > note',]},
    'issn': {'bs_exp':['mods > identifier[type=\"issn\"]',]},
    'lccn': {'bs_exp':['mods > identifier[type=\"lccn\"]',]},
    'oclcn': {'bs_exp':['mods > identifier[type=\"oclcn\"]',]},
    'depositor': {'bs_exp':['mods > name',]}
}

CATALOG_MONOGRAPH_ITEM_MODS_MAP = {
    'id': {'bs_exp':['recordIdentifier',]},
    'title':{'bs_exp':['mods > titleInfo:not([type]) > title', 'mods > titleInfo > subTitle', 'mods > titleInfo > nonSort',]},  # formatted as follows: [title]: [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['mods > titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['mods > titleInfo[type=\"alternative\"] > title',]},
    'creator': {'bs_exp':['mods > name',]},
    'contributor': {'bs_exp':['mods > name',]},
    'publication_place': {'bs_exp':['mods > originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['mods > originInfo > publisher', 'mods > name',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['mods > originInfo > dateIssued',]}, # without attributes
    'encoded_date': {'bs_exp':['mods > originInfo > dateIssued[encoding]',]}, # with encoding attribute; if contains attribute point="start" and point="end", group the values and split with a forward slash (/).
    'creation_date': {'bs_exp':['mods > originInfo > dateCreated', 'mods > originInfo > dateOther',]},
    'copyright_date': {'bs_exp':['mods > originInfo > copyrightDate',]},
    'edition': {'bs_exp':['mods > originInfo > edition',]},
    'issuance': {'bs_exp':['mods > originInfo > issuance',]},
    'frequency': {'bs_exp':['mods > originInfo > frequency',]},
    'language': {'bs_exp':['mods > language > languageTerm',]},
    'type_of_resource': {'bs_exp':['mods > typeOfResource',]},
    'format': {'bs_exp':['mods > physicalDescription > form',]},
    'extent': {'bs_exp':['mods > physicalDescription > extent',]},
    'genre': {'bs_exp':['*:not(relatedItem) > genre', ]}, # without parent of relatedItem; includes 'subject > genre'
    'abstract': {'bs_exp':['mods > abstract',]},
    'subject': {'bs_exp':['mods > subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo',]},
    'temporal_coverage': {'bs_exp':['mods > subject > temporal',]},
    'geographic_coverage': {'bs_exp':['mods > geographic', 'hierarchicalGeographic', 'cartographics', 'geographicCoordinates',]},
    'target_audience': {'bs_exp':['mods > targetAudience',]},
    'isbn': {'bs_exp':['mods > identifier[type=\"isbn\"]',]},
    'lccn': {'bs_exp':['mods > identifier[type=\"lccn\"]',]},
    'oclccn': {'bs_exp':['mods > identifier[type=\"oclc\"]',]},
    'url': {'bs_exp':['mods > location > url',]}
}

DIGITAL_MONOGRAPH_ITEM_MODS_MAP = {
    'id': {'bs_exp':['recordIdentifier',]},
    'title':{'bs_exp':['mods > titleInfo:not([type]) > title', 'mods > titleInfo > subTitle', 'mods > titleInfo > nonSort',]},  # formatted as follows: [title]: [subTitle], [nonSort]
    'uniform_title': {'bs_exp':['mods > titleInfo[type=\"uniform\"] > title',]},
    'alternative_title': {'bs_exp':['mods > titleInfo[type=\"alternative\"] > title',]},
    'creator': {'bs_exp':['mods > name',]},
    'contributor': {'bs_exp':['mods > name',]},
    'publication_place': {'bs_exp':['mods > originInfo > place > placeTerm[type=\"text\"]',]},
    'publisher': {'bs_exp':['mods > originInfo > publisher', 'mods > name',]}, # also 'name > namePart' with role > roleTerm="publisher"
    'publication_date': {'bs_exp':['mods > originInfo > dateIssued',]}, # without attributes
    'encoded_date': {'bs_exp':['mods > originInfo > dateIssued',]}, # with encoding attribute; if has attribute @point="start" and point="end", group the values and split with a forward slash (/).
    'creation_date': {'bs_exp':['mods > originInfo > dateCreated', 'mods > originInfo > dateOther',]},
    'copyright_date': {'bs_exp':['mods > originInfo > copyrightDate',]},
    'edition': {'bs_exp':['mods > originInfo > edition',]},
    'issuance': {'bs_exp':['mods > originInfo > issuance',]},
    'frequency': {'bs_exp':['mods > originInfo > frequency',]},
    'language': {'bs_exp':['mods > language > languageTerm',]},
    'type_of_resource': {'bs_exp':['mods > typeOfResource',]},
    'format': {'bs_exp':['mods > physicalDescription > form',]},
    'extent': {'bs_exp':['mods > physicalDescription > extent',]},
    'genre': {'bs_exp':['*:not(relatedItem) > genre', ]}, # without parent of relatedItem; includes 'subject > genre'
    'abstract': {'bs_exp':['mods > abstract',]},
    'subject': {'bs_exp':['mods > subject > topic', 'subject > name', 'subject > occupation', 'subject > titleInfo',]},
    'temporal_coverage': {'bs_exp':['mods > subject > temporal',]},
    'geographic_coverage': {'bs_exp':['mods > geographic', 'hierarchicalGeographic', 'cartographics', 'geographicCoordinates',]},
    'target_audience': {'bs_exp':['mods > targetAudience',]},
    'isbn': {'bs_exp':['mods > identifier[type=\"isbn\"]',]},
    'lccn': {'bs_exp':['mods > identifier[type=\"lccn\"]',]},
    'oclccn': {'bs_exp':['mods > identifier[type=\"oclc\"]',]},
    'url': {'bs_exp':['mods > location > url',]},
    'depositor': {'bs_exp':['mods > name',]} # with role > roleTerm="depositor"
}

# mappings between base layer fields and BeautifulSoup selectors for RELS-EXT

DIGITAL_COLLECTION_RDF_MAP = {
    'coll_id': {'bs_exp':['Description',]},
    'collection_id': {'bs_exp':['Description > isMemberOfCollection',]},
}

DIGITAL_ITEM_RDF_MAP = {
    'item_id': {'bs_exp':['Description',]},
    'collection_id': {'bs_exp':['Description > isMemberOfCollection',]},
}
