import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.provbz.helpers as helpers

from ckan.lib.base import model
from pylons.i18n.translation import get_lang

import ckanext.provbz.model.custom as custom

log = logging.getLogger(__name__)

class PBZThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):

    '''
    The Provincia di Bolzano theme plugin.
    '''

    custom_fields = [
        ['holder'], 
        ['sector'], 
        ['geographical_coverage'], 
        ['temporal_coverage'], 
        ['geographical_min_level'], 
        ['publication_date'], 
        ['update_type'], 
        ['update_text'],  
        ['base_year'], 
        ['encoding']
    ]

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IPackageController, inherit=True)


    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

    def _modify_package_schema(self, schema):
        for field in self.custom_fields:
            schema.update({
                field[0]: [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')
                ]
            })

        return schema

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(PBZThemePlugin, self).create_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(PBZThemePlugin, self).update_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(PBZThemePlugin, self).show_package_schema()

        for field in self.custom_fields:
            schema.update({
                field[0]: [
                    toolkit.get_converter('convert_from_extras'), 
                    toolkit.get_validator('ignore_missing')
                ]
            })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # see the ITemplateHelpers plugin interface.
    def get_helpers(self):
        return {
            'recent_updates': helpers.recent_updates,
            'get_default_locale': helpers.get_default_locale,
            'get_locale': helpers.get_locale,
            'getLocalizedPageLink': helpers.getLocalizedPageLink,
            'parseRefDate': helpers.parseRefDate,
            'get_news_preview': helpers.get_news_preview,
            'getLocalizedFieldValue': helpers.getLocalizedFieldValue
            #'get_custom_categories_list': helpers.get_custom_categories_list
        }

    def before_map(self, map):
        map.connect('/privacy', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzprivacy')
        map.connect('/legal', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzlegal')
        map.connect('/faq', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzfaq')
        map.connect('/info', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzinfo')
        map.connect('/acknowledgements', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzacknowledgements')
        return map
        
    def after_map(self, route_map):
        return route_map

    def after_create(self, context, pkg_dict):
        #if not custom.custom_field_table.exists():
        #    custom.init_db()

        # During the harvest the get_lang() is not defined
        if get_lang():
            lang = get_lang()[0]
            
            for extra in pkg_dict.get('extras'):
                for field in self.custom_fields:
                    if extra.get('key') == field[0]:
                        log.info(':::::::::::::::Localizing custom field: %r', field[0])
                        
                        # Create the localized field record
                        self.createLocField(extra, lang, pkg_dict.get('id'))

    def after_update(self, context, pkg_dict):
        #if not custom.custom_field_table.exists():
        #    custom.init_db()

        # During the harvest the get_lang() is not defined
        if get_lang():
            lang = get_lang()[0]
            
            for extra in pkg_dict.get('extras'):
                for field in self.custom_fields:
                    if extra.get('key') == field[0]:
                        log.info(':::::::::::::::Localizing custom field: %r', field[0])
                        f = custom.get_field(extra.get('key'), pkg_dict.get('id'), lang)
                        if f:
                            if extra.get('value') == '':
                                f.purge()
                            elif f.text != extra.get('value'):
                                # Update the localized field value for the current language
                                f.text = extra.get('value')
                                f.save()

                                log.info('Custom field updated successfully')

                        elif extra.get('value') != '':
                            # Create the localized field record
                            self.createLocField(extra, lang, pkg_dict.get('id'))

    def createLocField(self, extra, lang, packege_id): 
        log.debug(':::::::::::::::::::::::: %r', str(packege_id))

        new_loc_field = custom.CustomFieldMultilang(packege_id, extra.get('key'), lang, extra.get('value'))
        custom.CustomFieldMultilang.save(new_loc_field)

        log.info('Custom field created successfully')
        