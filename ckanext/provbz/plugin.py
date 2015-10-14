import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.provbz.helpers as helpers

class PBZThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''An example theme plugin.
    '''

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

    def _modify_package_schema(self, schema):
        schema.update({
            'holder': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'sector': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'geographical_coverage': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'temporal_coverage': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'geographical_min_level': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'publication_date': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'update_type': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'update_text': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'base_year': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
        })

        schema.update({
            'encoding': [toolkit.get_validator('ignore_missing'),
                   toolkit.get_converter('convert_to_extras')]
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
        schema.update({
            'holder': [toolkit.get_converter('convert_from_extras'), 
                      toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'sector': [toolkit.get_converter('convert_from_extras'), 
                      toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'geographical_coverage': [toolkit.get_converter('convert_from_extras'), 
                                       toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'temporal_coverage': [toolkit.get_converter('convert_from_extras'), 
                                       toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'geographical_min_level': [toolkit.get_converter('convert_from_extras'), 
                                     toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'publication_date': [toolkit.get_converter('convert_from_extras'), 
                                toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'update_type': [toolkit.get_converter('convert_from_extras'), 
                           toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'update_text': [toolkit.get_converter('convert_from_extras'), 
                            toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'base_year': [toolkit.get_converter('convert_from_extras'), 
                           toolkit.get_validator('ignore_missing')]
        })

        schema.update({
            'encoding': [toolkit.get_converter('convert_from_extras'),
                        toolkit.get_validator('ignore_missing')]
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
            'get_news_preview': helpers.get_news_preview
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