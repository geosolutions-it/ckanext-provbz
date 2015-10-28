
import logging
import ckan.lib.base as base

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