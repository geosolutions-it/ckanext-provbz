
import logging

from ckan import model
from ckan.model import Session

from ckan.plugins.core import SingletonPlugin

from ckanext.multilang.harvesters.multilang import MultilangHarvester
from ckanext.geonetwork.harvesters.geonetwork import GeoNetworkHarvester

log = logging.getLogger(__name__)


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
