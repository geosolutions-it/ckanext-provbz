import logging
import operator

import ckan
import ckan.model as model
import ckan.plugins as p
import ckan.lib.search as search
import ckan.lib.helpers as h

import ckan.logic as logic

NUM_TOP_PUBLISHERS = 6
NUM_MOST_VIEWED_DATASETS = 10

log = logging.getLogger(__file__)


def recent_updates(n):
    '''
    Return a list of the n most recently updated datasets.
    '''
    log.debug(':::::::::::::::::::::::::::::::::: %r' % n)
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

    log.info('Found %d recent updates:::::::: ' % len(search_results))
    log.info('Updates:::::::::::::::::::::::  %r ' % search_results)
	
    return search_results.get('results', [])
