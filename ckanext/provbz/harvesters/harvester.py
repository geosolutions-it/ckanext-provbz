
import logging

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
            super_package_dicts.append(c.get_package_dict(iso_values, harvest_object))
            if hasattr(c, '_package_dict'):
                    self._package_dict = c._package_dict

        package_dict = None
        for _dict in super_package_dicts:
            if package_dict:
                extras = package_dict.get('extras')

                for item in _dict.get('extras'):
                    if item not in extras:
                        extras.append(item)

                package_dict['extras'] = extras
            else:
                package_dict = _dict

        # End of processing, return the modified package
        return package_dict

    def after_import_stage(self, package_dict):
        for cls in PBZHarvester.__bases__:
            c = cls()
            if hasattr(c, '_package_dict'):
                    c._package_dict = self._package_dict
                    c.after_import_stage(package_dict)
