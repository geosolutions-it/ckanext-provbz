
import logging
import re

from datetime import datetime

from ckan import model
from ckan.model import Session

from ckanext.multilang.model import PackageMultilang, TagMultilang

from ckan.plugins.core import SingletonPlugin

from ckanext.multilang.harvesters.multilang import MultilangHarvester
from ckanext.geonetwork.harvesters.geonetwork import GeoNetworkHarvester

from ckanext.spatial.model import ISODocument
from ckanext.spatial.model import ISOElement
from ckanext.spatial.model import ISOKeyword

from ckanext.multilang.harvesters.multilang import ISOTextGroup

log = logging.getLogger(__name__)

class ISOCharacterSet(ISOElement):
    elements = [
        ISOElement(
            name="code",
            search_paths=[
                "gmd:MD_CharacterSetCode/@codeListValue"
            ],
            multiplicity="0..1"
        )
    ]

ISODocument.elements.append(
    ISOCharacterSet(
        name="character-set",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet"
        ],
        multiplicity="*"
    ))

ISODocument.elements.append(
    ISOElement(
        name="conformity-specification-title",
        search_paths=[
            "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:title/gco:CharacterString/text()"
        ],
        multiplicity="1",
     ))

ISODocument.elements.append(
    ISOTextGroup(
        name="conformity-title-text",
        search_paths=[
            "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:title/gmd:PT_FreeText/gmd:textGroup"
        ],
        multiplicity="1..*",
    ))

ISOKeyword.elements.append(
    ISOElement(
        name="thesaurus-title",
        search_paths=[
            "gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()",
        ],
        multiplicity="1",
    ))

ISOKeyword.elements.append(
    ISOElement(
        name="thesaurus-identifier",
        search_paths=[
            "gmd:thesaurusName/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
        ],
        multiplicity="1",
    ))


class PBZHarvester(GeoNetworkHarvester, MultilangHarvester):

    ## Temporarily mapping: frequencies must be changed CSW side
    _mapping_frequencies_to_mdr_vocabulary = {
        'biannually' : 'BIENNIAL',
        'asNeeded' : 'IRREG',
        'quarterly' : 'QUARTERLY',
        'fortnightly' : 'BIWEEKLY',
        'annually' : 'ANNUAL',
        'monthly' : 'MONTHLY',
        'weekly' : 'WEEKLY',
        'daily' : 'DAILY',
        'continual' : 'CONT',
        'notPlanned' : 'UNKNOWN',
        'irregular' : 'IRREG',
        'unknown' : 'UNKNOWN'
    }

    _mapping_languages_to_mdr_vocabulary = {
        'ita': 'ITA',
        'ger': 'DEU',
        'eng': 'ENG'
    }

    _default_values = {
        'dataset_theme': 'OP_DATPRO',
        'dataset_language': '{ITA,DEU}',
        'agent_code': 'p_bz',
        'frequency': 'UNKNOWN',
        'agent_code_regex': '\(([^)]+)\)',
        'org_name_regex': '-(.+)'
    }    

    def info(self):
        return {
            'name': 'Provincia Di Bolzano',
            'title': 'PBZ CSW server',
            'description': 'Provincia di Bolzano Harvester for CWS',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, iso_values, harvest_object):        
        super_package_dicts = []
        for cls in PBZHarvester.__bases__:
            c = cls()
            
            if hasattr(c, 'source_config'):
                c.source_config = self.source_config

            super_package_dicts.append(c.get_package_dict(iso_values, harvest_object))

            if hasattr(c, '_package_dict'):
                    self._package_dict = c._package_dict

            if hasattr(c, '_ckan_locales_mapping'):
                    self._ckan_locales_mapping = c._ckan_locales_mapping

        mapping_frequencies_to_mdr_vocabulary = self.source_config.get('mapping_frequencies_to_mdr_vocabulary', self._mapping_frequencies_to_mdr_vocabulary)
        mapping_languages_to_mdr_vocabulary = self.source_config.get('mapping_languages_to_mdr_vocabulary', self._mapping_languages_to_mdr_vocabulary)
        
        default_values = self.source_config.get('default_values', None)
        if default_values and not all(name in default_values for name in self._default_values):
            default_values = self._default_values
            log.warning('Some keys are missing in default_values configuration property, keyes to use are: dataset_theme, dataset_language, agent_code, frequency. Using defaults')
        elif not default_values:
            default_values = self._default_values

        # Merging metadata extras
        package_dict = None
        for _dict in super_package_dicts:
            if package_dict:
                extras = package_dict.get('extras')

                for item in _dict.get('extras'):
                    if item not in extras:
                        extras.append(item)

                package_dict['extras'] = extras 

                ## Configuring package organizations         
                organisation_mapping = self.source_config.get('organisation_mapping', [])

                if organisation_mapping:
                    if package_dict.get('owner_org') != _dict.get('owner_org'):
                        source_dataset = model.Package.get(harvest_object.source.id)
                        if source_dataset.owner_org:
                            if _dict.get('owner_org') != source_dataset.owner_org:
                                package_dict['owner_org'] =_dict.get('owner_org')
            else:
                package_dict = _dict
                
        # ---------------------------------------------------
        # MANDATORY FOR DCAT-AP_IT
        # ---------------------------------------------------
        
        # identifier
        # ##################
        identifier = iso_values["guid"]
        package_dict['extras'].append({'key': 'identifier', 'value': identifier})

        default_agent_code = identifier.split(':')[0] if ':' in identifier else default_values.get('agent_code')

        # theme
        # ##################
        if iso_values["keywords"]:
            log.debug('::::: Collecting thesaurus data for dcatapit skos theme from the metadata keywords :::::')

            dcatapit_skos_theme_id = self.source_config.get('dcatapit_skos_theme_id', 'theme.data-theme-skos')
            dataset_themes = []
            for key in iso_values["keywords"]:
            	if dcatapit_skos_theme_id and dcatapit_skos_theme_id in key['thesaurus-identifier']:            		
            		for k in key['keyword']:
            			query = Session.query(TagMultilang).filter(TagMultilang.text==k)
            			query = query.autoflush(True)
            			theme = query.first()

            			dataset_themes.append(theme.tag_name)

            if dataset_themes and len(dataset_themes) > 0:
            	dataset_themes = '{' + ','.join(str(l) for l in dataset_themes) + '}'
            else:
            	dataset_themes =  default_values.get('dataset_theme')

            log.info("Medatata harvested dataset themes: %r", dataset_themes)
            package_dict['extras'].append({'key': 'theme', 'value': dataset_themes})
        else:
            package_dict['extras'].append({'key': 'theme', 'value':  default_values.get('dataset_theme')})

        # publisher
        # ##################
        citedResponsiblePartys = iso_values["cited-responsible-party"]
        self.localized_publisher = []

        for party in citedResponsiblePartys:
            if party["role"] == "publisher":
                publisher_name = party["organisation-name"]

            	agent_code, organization_name = self.get_agent(publisher_name, default_values)

                package_dict['extras'].append({'key': 'publisher_name', 'value': organization_name or publisher_name})

                if publisher_name:
                    package_dict['extras'].append({'key': 'publisher_identifier', 'value': agent_code or default_agent_code})

                self.localized_publisher.append({
                    'text':  organization_name or publisher_name,
                    'locale': self._ckan_locales_mapping[iso_values["metadata-language"].lower()]
                })

                for entry in party["organisation-name-localized"]:
                    if entry['text'] and entry['locale'].lower()[1:]:
                    	agent_code, organization_name = self.get_agent(entry['text'], default_values)

                        if self._ckan_locales_mapping[entry['locale'].lower()[1:]]:
                            self.localized_publisher.append({
                                'text': organization_name or entry['text'],
                                'locale': self._ckan_locales_mapping[entry['locale'].lower()[1:]]
                            })
                        else:
                            log.warning('Locale Mapping not found for dataset publisher name, entry skipped!')
                    else:
                        log.warning('TextGroup data not available for dataset publisher name, entry skipped!')

        # modified
        # ##################
        revision_date = iso_values["date-updated"]
        package_dict['extras'].append({'key': 'modified', 'value': revision_date})

        # frequency
        # ##################
        updateFrequency = iso_values["frequency-of-update"]
        package_dict['extras'].append({'key': 'frequency', 'value': mapping_frequencies_to_mdr_vocabulary.get(updateFrequency, default_values.get('frequency'))})

        # rights_holder
        # ##################
        citedResponsiblePartys = iso_values["cited-responsible-party"]
        for party in citedResponsiblePartys:
            if party["role"] == "owner":
                rights_older_and_author = party["organisation-name"]

            	agent_code, organization_name = self.get_agent(rights_older_and_author, default_values)

                if rights_older_and_author:
                	package_dict['extras'].append({'key': 'holder_identifier', 'value': agent_code or default_agent_code})

                contact_info_online_resource = None
                if party["contact-info"] != '' and party["contact-info"]["online-resource"] and party["contact-info"]["online-resource"] != '':
                    contact_info_online_resource = party["contact-info"]["online-resource"].get('url')

                    package_dict['extras'].append({'key': 'site_url', 'value': contact_info_online_resource})
                    package_dict['url'] = contact_info_online_resource

                    package_dict['extras'].append({'key': 'contact', 'value': party["contact-info"]["email"] or None})

                package_dict['extras'].append({'key': 'holder_name', 'value': organization_name or rights_older_and_author})

                package_dict['author'] = organization_name or rights_older_and_author

                self.localized_org = []

                self.localized_org.append({
                    'text': organization_name or rights_older_and_author,
                    'locale': self._ckan_locales_mapping[iso_values["metadata-language"].lower()]
                })

                for entry in party["organisation-name-localized"]:
                    if entry['text'] and entry['locale'].lower()[1:]:
                    	agent_code, organization_name = self.get_agent(entry['text'], default_values)

                        if self._ckan_locales_mapping[entry['locale'].lower()[1:]]:
                            self.localized_org.append({
                                'text': organization_name or entry['text'],
                                'locale': self._ckan_locales_mapping[entry['locale'].lower()[1:]]
                            })
                        else:
                            log.warning('Locale Mapping not found for organization name, entry skipped!')
                    else:
                        log.warning('TextGroup data not available for organization name, entry skipped!')

        # ---------------------------------------------------
        # OTHER NOT MANDATORY FOR DCAT_AP-IT
        # ---------------------------------------------------

        # alternate_identifier nothing to do 
        # ####################

        # issued
        # ##################
		publication_date = iso_values["date-released"]
        package_dict['extras'].append({'key': 'issued', 'value': publication_date})

        # geographical_name nothing to do 
        # #################

        # geographical_geonames_url nothing to do 
        # #########################
		
		# language
		# ############
        dataset_languages = iso_values["dataset-language"]
        language = None      
        if dataset_languages and len(dataset_languages) > 0:
        	languages = []
        	for language in dataset_languages:
        		languages.append(mapping_languages_to_mdr_vocabulary.get(language, None))

        	language = '{' + ','.join(str(l) for l in languages) + '}'
        	log.debug("Medatata harvested dataset languages: %r", language)
        else:
        	language = self.source_config.get('dataset_languages', default_values.get('dataset_language'))

        package_dict['extras'].append({'key': 'language', 'value': language})

        # temporal_coverage
        # ##################
        for key in ['temporal-extent-begin', 'temporal-extent-end']:
        	if len(iso_values[key]) > 0:
        		temporal_extent_value = iso_values[key][0]
        		if key == 'temporal-extent-begin':
        			package_dict['extras'].append({'key': 'temporal_start', 'value': temporal_extent_value})

        		if key == 'temporal-extent-end':
        			package_dict['extras'].append({'key': 'temporal_end', 'value': temporal_extent_value})

       	# conforms_to
       	# ##################
       	conforms_to = iso_values["conformity-specification-title"]
       	package_dict['extras'].append({'key': 'conforms_to', 'value': conforms_to})

       	self.localized_confomity = []

       	self.localized_confomity.append({
       		'text': conforms_to,
       		'locale': self._ckan_locales_mapping[iso_values["metadata-language"].lower()]
       	})

       	for entry in iso_values["conformity-title-text"]:
       		if entry['text'] and entry['locale'].lower()[1:]:
       			if self._ckan_locales_mapping[entry['locale'].lower()[1:]]:
       				self.localized_confomity.append({
       					'text': entry['text'],
       					'locale': self._ckan_locales_mapping[entry['locale'].lower()[1:]]
       				})
       			else:
       				log.warning('Locale Mapping not found for the conformity title, entry skipped!')
       		else:
       			log.warning('TextGroup data not available for the conformity title, entry skipped!')

        # creator
        # ###############
        citedResponsiblePartys = iso_values["cited-responsible-party"]
        self.localized_creator = []

        for party in citedResponsiblePartys:
            if party["role"] == "author":
            	creator_name = party["organisation-name"]

            	agent_code, organization_name = self.get_agent(creator_name, default_values)

            	package_dict['extras'].append({'key': 'creator_name', 'value': organization_name or creator_name})

                if creator_name:
                    package_dict['extras'].append({'key': 'creator_identifier', 'value': agent_code or default_agent_code})

                self.localized_creator.append({
                    'text':  organization_name or creator_name,
                    'locale': self._ckan_locales_mapping[iso_values["metadata-language"].lower()]
                })

                for entry in party["organisation-name-localized"]:
                    if entry['text'] and entry['locale'].lower()[1:]:
                    	agent_code, organization_name = self.get_agent(entry['text'], default_values)

                        if self._ckan_locales_mapping[entry['locale'].lower()[1:]]:
                            self.localized_creator.append({
                                'text': organization_name or entry['text'],
                                'locale': self._ckan_locales_mapping[entry['locale'].lower()[1:]]
                            })
                        else:
                            log.warning('Locale Mapping not found for dataset creator name, entry skipped!')
                    else:
                        log.warning('TextGroup data not available for dataset creator name, entry skipped!')

        # ---------------------------------------------------
        # OTHER FOR PROV-BZ
        # ---------------------------------------------------

        # creation_date
        # ##################
        creation_date = iso_values["date-created"]
        package_dict['extras'].append({'key': 'creation_date', 'value': creation_date})

        codes = []
        for char_set in iso_values["character-set"]:
            code = char_set["code"]
            if code:
                codes.append(code)

        # character_set
        # ##################
        character_set = " - ".join(codes)
        package_dict['extras'].append({'key': 'encoding', 'value': character_set})

        # OTHER FOR CKAN
        # ##############

        # ckan_license
        # ##################
        ckan_license = None
        use_constraints = iso_values.get('use-constraints')
        if use_constraints:
            use_constraints = use_constraints[0]
            import ckan.logic.action.get as _license
            license_list = _license.license_list({'model': model, 'session': Session, 'user': 'harvest'}, {})
            for license in license_list:
                if use_constraints == str(license.get('id')) or use_constraints == str(license.get('url')) or (str(license.get('id')) in use_constraints.lower()):
                    ckan_license = license
                    break

        if ckan_license:
            package_dict['license_id'] = ckan_license.get('id')
        else:
            default_license = self.source_config.get('default_license')
            if default_license:
                package_dict['license_id'] = default_license

        # End of processing, return the modified package
        return package_dict

    def get_agent(self, agent_string, default_values):
        agent_code = re.search(default_values.get('agent_code_regex'), agent_string)
        if agent_code:
    		agent_code = agent_code.group(1).lower().strip().split(":")[1]
    		agent_code = agent_code.lstrip()

        organization_name = re.search(default_values.get('org_name_regex'), agent_string)
        if organization_name:
    		organization_name = organization_name.group(1)
    		organization_name = organization_name.lstrip()

    	return [agent_code, organization_name]

    def after_import_stage(self, package_dict):
        for cls in PBZHarvester.__bases__:
            c = cls()
            if hasattr(c, '_package_dict'):
                    c._package_dict = self._package_dict
                    c.after_import_stage(package_dict)

        package_id = package_dict.get('id')

        try:
            ## PERSISTING the multilang fields
            ## -------------------------------

            for org in self.localized_org:
            	# persisting author field
            	self.persist_package_multilang_field(package_id, 'author', org.get('text'), org.get('locale'), 'package')

                # persisting holder_name field
                self.persist_package_multilang_field(package_id, 'holder_name', org.get('text'), org.get('locale'), 'extra')         	
            
            for conformity in self.localized_confomity:
            	# persisting author field
            	self.persist_package_multilang_field(package_id, 'conforms_to', conformity.get('text'), conformity.get('locale'), 'extra')

            for creator in self.localized_creator:
                # persisting author field
                self.persist_package_multilang_field(package_id, 'creator_name', creator.get('text'), creator.get('locale'), 'extra')

            for publisher in self.localized_publisher:
                # persisting author field
                self.persist_package_multilang_field(package_id, 'publisher_name', publisher.get('text'), publisher.get('locale'), 'extra') 
			
            pass
        except Exception, e:
            log.error('Exception occurred while persisting DB objects: %s', e)
            raise

    def persist_package_multilang_field(self, package_id, field_name, text, locale, field_type):
	    record = PackageMultilang.get(package_id, field_name, locale, field_type)
	    if record:
	        log.info('::::::::: Updating the localized {0} package field in the package_multilang table :::::::::'.format(field_name))
	        record.text = text
	        record.save()
	        log.info('::::::::: PACKAGE MULTILANG FIELD UPDATED SUCCESSFULLY :::::::::') 
	    else:
	        log.info('::::::::: Adding new localized {0} package field in the package_multilang table :::::::::'.format(field_name))
	        PackageMultilang.persist({'id': package_id, 'text': text, 'field': field_name}, locale, field_type)
	        log.info('::::::::: PACKAGE MULTILANG FIELD PERSISTED SUCCESSFULLY :::::::::')
