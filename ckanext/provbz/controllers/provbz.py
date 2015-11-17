
import logging
import ckan.lib.base as base

import cgi
from ckan.common import _, c, request, response
from  ckan.lib.helpers import json
from pylons import config

log = logging.getLogger(__name__)

class PROVBZController(base.BaseController):
	
    def provbzprivacy(self):
        return base.render('home/privacy.html')

    def provbzlegal(self):
        return base.render('home/legal.html')

    def provbzfaq(self):
        return base.render('home/faq.html')

    def provbzinfo(self):
        return base.render('home/info.html')

    def provbzacknowledgements(self):
        return base.render('home/acknowledgements.html')

    def provbzformats(self):
        return base.render('home/formats.html')

    def status(self):
        request_headers = request.headers
        log.debug('Request Headers: %r', request_headers)

        accept_language = request_headers['Accept-Language']
        log.debug('Accept-Language: %r', accept_language)

        languages = accept_language.split(',')
        
        locale_q_pairs = []

        for language in languages:
            if language.split(";")[0] == language:
                # no q => q = 1
                locale_q_pairs.append((language.strip(), "1"))
            else:
                locale = language.split(";")[0].strip()
                q = language.split(";")[1].split("=")[1]
                locale_q_pairs.append((locale, q))

        log.debug('Locale Q-Pairs: %r', locale_q_pairs)

        json_response = {}
        
        locale_default = config.get('ckan.locale_default')
        log.debug('Ckan locale_default: %r', locale_default)

        locales_offered = config.get('ckan.locales_offered').split()
        log.debug('Ckan locale_order: %r', locales_offered)

        for pair in locale_q_pairs:
            if pair[0] in locales_offered:
                json_response["availableLocales"] = locales_offered
                json_response["isDefaultLocale"] = (pair[0] == locale_default)
                json_response["locale"] = pair[0]

                return json.dumps(json_response)

        return '{}'