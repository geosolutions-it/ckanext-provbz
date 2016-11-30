import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.provbz.helpers as helpers

from ckan.lib.base import model
from pylons.i18n.translation import get_lang

import ckanext.provbz.model.custom as custom

import ckanext.dcatapit.interfaces as interfaces

from ckan.common import _, ungettext

try:
    from ckan.lib.plugins import DefaultTranslation
except ImportError:
    class DefaultTranslation():
        pass

log = logging.getLogger(__name__)

class PBZThemePlugin(plugins.SingletonPlugin, DefaultTranslation):

    '''
    The Provincia di Bolzano theme plugin.
    '''

    # IConfigurer
    plugins.implements(plugins.IConfigurer)

    # ITemplateHelpers
    plugins.implements(plugins.ITemplateHelpers)

    # IRoutes
    plugins.implements(plugins.IRoutes)

    # IPackageController
    plugins.implements(plugins.IPackageController, inherit=True)

    # ICustomSchema
    plugins.implements(interfaces.ICustomSchema)

    # ITranslation
    if toolkit.check_ckan_version(min_version='2.5.0'):
        plugins.implements(plugins.ITranslation, inherit=True)

    # Implementation of ICustomSchema
    # ------------------------------------------------------------

    def get_custom_schema(self):
        return [
            {
                'name': 'creation_date',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'date',
                'label': _('Creation Date'),
                'placeholder': _('creation date'),
                'is_required': False,
                'localized': False
            },  {
                'name': 'encoding',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'text',
                'label': _('Encoding'),
                'placeholder': _('encoding type'),
                'is_required': False,
                'localized': False
            }, {
                'name': 'site_url',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'url',
                'label': _('Site URL'),
                'placeholder': _('site url'),
                'is_required': False,
                'localized': True
            }, {
                'name': 'contact',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'email',
                'label': _('Contact'),
                'placeholder': _('contact'),
                'is_required': False,
                'localized': True
            }
        ]

    # Implementation of ICustomSchema
    # ------------------------------------------------------------

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('public/base', 'ckanext-provbz')

    # Implementation of ITemplateHelpers
    # ------------------------------------------------------------

    def get_helpers(self):
        return {
            'recent_updates': helpers.recent_updates,
            'get_default_locale': helpers.get_default_locale,
            'get_locale': helpers.get_locale,
            'getLocalizedPageLink': helpers.getLocalizedPageLink,
            'parseRefDate': helpers.parseRefDate,
            'get_news_preview': helpers.get_news_preview,
            'getLocalizedFieldValue': helpers.getLocalizedFieldValue,
            'getLocalizedTagName': helpers.getLocalizedTagName,
            'checkForShibboletURL': helpers.checkForShibboletURL
            #'get_custom_categories_list': helpers.get_custom_categories_list
        }

    # Implementation of IRoute
    # ------------------------------------------------------------

    def before_map(self, map):
        map.connect('/privacy', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzprivacy')
        map.connect('/legal', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzlegal')
        map.connect('/faq', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzfaq')
        map.connect('/info', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzinfo')
        map.connect('/acknowledgements', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzacknowledgements')
        map.connect('/formats', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='provbzformats')
        
        ## Used as utility end-point to manage cookies messages and the automatic locale setting
        map.connect('/loc_status', controller='ckanext.provbz.controllers.provbz:PROVBZController', action='status')
        
        return map
        
    def after_map(self, route_map):
        return route_map

    # Implementation of IPackageController
    # ------------------------------------------------------------

    def after_create(self, context, pkg_dict):
        #if not custom.custom_field_table.exists():
        #    custom.init_db()

        # During the harvest the get_lang() is not defined
        if get_lang():
            lang = get_lang()[0]
            
            for extra in pkg_dict.get('extras'):
                for field in self.get_custom_schema():
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
                for field in self.get_custom_schema():
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

    def createLocField(self, extra, lang, package_id): 
        log.debug('Creating createLocField for package ID: %r', str(package_id))

        new_loc_field = custom.CustomFieldMultilang(package_id, extra.get('key'), lang, extra.get('value'))
        custom.CustomFieldMultilang.save(new_loc_field)

        log.info('Custom field created successfully')
        