
import logging

from ckan import model
from ckan.model import Session

from ckanext.multilang.model import PackageMultilang

from ckan.plugins.core import SingletonPlugin

from ckanext.multilang.harvesters.multilang import MultilangHarvester
from ckanext.geonetwork.harvesters.geonetwork import GeoNetworkHarvester

from ckanext.spatial.model import ISODocument
from ckanext.spatial.model import ISOElement

import ckanext.provbz.model.custom as custom

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
        multiplicity="0..*"
    )
)

class PBZHarvester(GeoNetworkHarvester, MultilangHarvester):

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
        
        # Custom fields (default metadata) harvestng
        updateFrequency = iso_values["frequency-of-update"]
        package_dict['extras'].append({'key': 'update_frequency', 'value': updateFrequency})

        creation_date = iso_values["date-created"]
        package_dict['extras'].append({'key': 'creation_date', 'value': creation_date})

        publication_date = iso_values["date-released"]
        package_dict['extras'].append({'key': 'publication_date', 'value': publication_date})

        revision_date = iso_values["date-updated"]
        package_dict['extras'].append({'key': 'revision_date', 'value': revision_date})

        codes = []
        for char_set in iso_values["character-set"]:
            code = char_set["code"]
            if code:
                codes.append(code)

        character_set = " - ".join(codes)
        package_dict['extras'].append({'key': 'encoding', 'value': character_set})

        citedResponsiblePartys = iso_values["cited-responsible-party"]
        for party in citedResponsiblePartys:
            if party["role"] == "owner":

                contact_info_online_resource = None
                if party["contact-info"]["online-resource"] and party["contact-info"]["online-resource"] != '':
                    contact_info_online_resource = party["contact-info"]["online-resource"].get('url')
                    package_dict['extras'].append({'key': 'site_url', 'value': contact_info_online_resource})
                    package_dict['url'] = contact_info_online_resource

                package_dict['extras'].append({'key': 'contact', 'value': party["contact-info"]["email"] or None})

                package_dict['extras'].append({'key': 'holder', 'value': party["organisation-name"]})

                # Default value to populate the package table too during the harvest
                package_dict['author'] = party["organisation-name"]

                # Collecting the localized author's organizations. The aim is to assign to the author field is org name in metadata (which is localized)
                self.localized_org = []

                self.localized_org.append({
                    'text': party["organisation-name"],
                    'locale': self._ckan_locales_mapping[iso_values["metadata-language"].lower()]
                })

                for entry in party["organisation-name-localized"]:
                    if entry['text'] and entry['locale'].lower()[1:]:
                        if self._ckan_locales_mapping[entry['locale'].lower()[1:]]:
                            self.localized_org.append({
                                'text': entry['text'],
                                'locale': self._ckan_locales_mapping[entry['locale'].lower()[1:]]
                            })
                        else:
                            log.warning('Locale Mapping not found for organization name, entry skipped!')
                    else:
                        log.warning('TextGroup data not available for organization name, entry skipped!')

        # Check for metadata license
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

    def after_import_stage(self, package_dict):
        for cls in PBZHarvester.__bases__:
            c = cls()
            if hasattr(c, '_package_dict'):
                    c._package_dict = self._package_dict
                    c.after_import_stage(package_dict)

        package_id = package_dict.get('id')

        log.debug("::::::::::::: Persisting localized Author package field :::::::::::::")     

        try:
            session = Session

            rows = session.query(PackageMultilang).filter(PackageMultilang.package_id == package_id, PackageMultilang.field == 'author').all()

            if not rows:
                log.info('::::::::: Adding new localized organization author in the package_multilang table :::::::::')
                
                log.debug('::::: Persisting organization author metadata locale :::::')

                for org in self.localized_org:
                    session.add_all([
                        PackageMultilang(package_id=package_id, field='author', field_type='localized', lang=org.get('locale'), text=org.get('text')),
                    ])

                    # This for the holder custom field
                    new_holder_loc_field = custom.CustomFieldMultilang(package_id, 'holder', org.get('locale'), org.get('text'))
                    custom.CustomFieldMultilang.save(new_holder_loc_field)

                session.commit()

                log.info('::::::::: OBJECT PERSISTED SUCCESSFULLY :::::::::')

            else:
                log.info('::::::::: Updating localized organization author in the package_multilang table :::::::::')
                for row in rows:
                    if row.field == 'author': 
                        for org in self.localized_org:
                            if org.get('locale') == row.lang:
                                row.text = org.get('text')

                    row.save()

                log.info('::::::::: OBJECT UPDATED SUCCESSFULLY :::::::::') 

            pass
        except Exception, e:
            # on rollback, the same closure of state
            # as that of commit proceeds. 
            session.rollback()

            log.error('Exception occurred while persisting DB objects: %s', e)
            raise