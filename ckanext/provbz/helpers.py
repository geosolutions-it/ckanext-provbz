import logging
import operator
import json

import ckan
import ckan.model as model
import ckan.plugins as p
import ckan.lib.search as search
import ckan.lib.helpers as h

import ckan.logic as logic

from pylons import config

from pylons.i18n.translation import get_lang
from ckanext.multilang.model import PackageMultilang

import ckanext.provbz.model.custom as custom

import ckanext.pages.db as db


log = logging.getLogger(__file__)


def get_default_locale():
    locale_default = config.get('ckan.locale_default')

    log.debug('Retrieving Ckan default locale: %r', locale_default)
    return locale_default

def get_locale():
    lang = get_lang()[0]

    log.info('Retrieving Ckan current locale: %r', lang)
    return lang

def getLocalizedPageLink(page):
    locale = get_lang()[0]

    if(page):
        url = "/" + locale + "/" + page

    return url

def parseRefDate(references):
    j = json.loads(references)
    return j

def get_news_preview(page):
    lang = get_lang()[0]

    log.info('Retrieving News page preview for current locale: %r', lang)

    news_page = db.Page.get(name=page, lang=lang)
    if news_page:
        news_page = db.table_dictize(news_page, {})
    return news_page

def recent_updates(n):
    #
    # Return a list of the n most recently updated datasets.
    #
    log.debug('::::: Retrrieving latest datasets: %r' % n)
    context = {'model': model,
               'session': model.Session,
               'user': p.toolkit.c.user or p.toolkit.c.author}

    data_dict = {'rows': n, 'sort': u'metadata_modified desc', 'facet': u'false'}
	
    try:
        search_results = logic.get_action('package_search')(context, data_dict)
    except search.SearchError, e:
        log.error('Error searching for recently updated datasets')
        log.error(e)
        search_results = {}

    for item in search_results.get('results'):
        log.info(':::::::::::: Retrieving the corresponding localized title and abstract :::::::::::::::')

        lang = get_lang()[0]
        
        q_results = model.Session.query(PackageMultilang).filter(PackageMultilang.package_id == item.get('id'), PackageMultilang.lang == lang).all() 

        if q_results:
            for result in q_results:
                item[result.field] = result.text

    log.debug('Found %d recent updates:::::::: ' % len(search_results))
    log.debug('Updates:::::::::::::::::::::::  %r ' % search_results)
	
    return search_results.get('results', [])

def getLocalizedFieldValue(field=None, pkg_dict=None):
    if field and pkg_dict:
        lang = get_lang()[0]
        localized_value = custom.get_field(field, pkg_dict.get('id'), lang)
        if localized_value:
            return localized_value.text
        else:
            return None
    else:
        return None

'''	
def get_custom_categories_list(items):
    #
    # Return the list of the categories tree
    #
	
    ##log.debug(':::::::::::::::::::::::::::::::::: %r' % items)
	
    context = {}
    data_dict = {'sort': 'packages', 'all_fields': 1}
    groups = logic.get_action('group_list')(context, data_dict)
	
    fnames = []
    for facet in items:
        fnames.append(facet['display_name'])
    	##log.info('::::::::::::::::::::::::::: %r', facet['display_name'])
	
    for group in groups:
	##log.info('::::::::::::::::::::::::::: %r', group)
    	d_name = group['display_name']

	if d_name not in fnames:
        	new_facet = {
			'display_name': d_name,
			'count': 0,
			'active': False,
                        'disabled': True,
			'name': group['name']
		}

		items.append(new_facet)
		
        base_pianification = []
        nature_habitat = []
        population_economy = []
        other = []

        active = False
        for item in items:
                name = item.get('name')
                if active is not True:
                        active = item.get('active')

                if name == 'transportation' or name == 'utilitiescommunication' or name == 'farming':
                        population_economy.append(item)
                elif name == 'climatologymeteorologyatmosphere' or name == 'environment' or name == 'geoscientificinformation' or name == 'inlandwaters':
                        nature_habitat.append(item)
                elif name == 'boundaries' or name == 'elevation' or name == 'imagerybasemapsearthcover' or name == 'planningcadastre':
                        base_pianification.append(item)
                else:
                        other.append(item)

    facets = []
    facets.append({'name': 'population_economy', 'items': population_economy})
    facets.append({'name': 'nature_habitat', 'items': nature_habitat})
    facets.append({'name': 'base_pianification', 'items': base_pianification})
    facets.append({'name': 'other', 'items': other})

    return {'active': active, 'facets_list': facets}
'''

