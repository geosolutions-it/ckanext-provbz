--------------
ckanext-provbz
--------------

The ckanext-provbz CKAN's extension provide some customizations for the CKAN Look and Feel.
In addition this extension provides an harvester that merge functionalities between two other 
harvesters built on the ckanext-spatial extension like:

- https://github.com/geosolutions-it/ckanext-multilang
- https://github.com/geosolutions-it/ckanext-geonetwork

------------
Requirements
------------

The ckanext-provbz extension has been developed for CKAN 2.4.
Other extensions needed as dependencies are:

- https://github.com/geosolutions-it/ckanext-multilang
- https://github.com/geosolutions-it/ckanext-geonetwork
- https://github.com/geosolutions-it/ckanext-pages

------------------------
Development Installation
------------------------

To install ckanext-provbz:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Go into your CKAN path for extension (like /usr/lib/ckan/default/src)

3. git clone https://github.com/geosolutions-it/ckanext-provbz

4. cd ckanext-provbz

5. python setup.py develop

6. Add ``provbz_theme``  and ``provbz_harvester`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

7. The ckanext-provbz extension provides some updates for the i18n files for 'it' and 'de' languages. Locale files in CKAN (.mo and .po) for these languages must be replaced with files located in this extension at the ckanext-provbz/ckanext/provbz/i18n/ path.

8. Update the production.ini configuration finding the default property ``licenses_group_url`` and change the value:

     licenses_group_url = file:///usr/lib/ckan/default/src/ckanext-provbz/ckanext/provbz/licenses/ckan.json

9. Restart CKAN.

----------------------
Harvest Configuration
----------------------

Using the ckanext-provbz harvester you can use an additional configuration property in addition to the other allowed for the ckanext-geonetwork and ckanext-multilang harvesters:

* ``default_license``: with this property you can specify the default license to use for the CKAN's dataset if none useLimitation has been found into the metadata. Below an example:

          {
            "default_license": "cc-zero"
          }

Below the complete configuration to use:

          {
               "private_datasets": "False", 
               "version": "2.6", 
               "harvest_iso_categories": "True",
               "default_extras": {
                    "geocat_layer_url": "http://geocatalogo.retecivica.bz.it/geokatalog/#!home&layer="
               },
               "organisation_mapping": [
                    {"key": "pab-foreste" ,"value": "Ufficio 32.3 - Ufficio Pianificazione forestale"},
                    {"key": "comune-bolzano-sistema-informativo-territoriale" ,"value": "Ufficio Sistema Informativo Territoriale, Comune di Bolzano"},
                    {"key": "pab-agenzia-provinciale-per-l-ambiente" ,"value": "Ripartizione 29 - Agenzia provinciale per l'ambiente"},
                    {"key": "pab-servizio-strade" ,"value": "Ripartizione 12 - Servizio Strade"},
                    {"key": "pab-protezione-antincendi-e-civile" ,"value": "Ripartizione 26 - Protezione antincendi e civile"},
                    {"key": "pab-natura-paesaggio-e-sviluppo-del-territorio" ,"value": "Ripartizione 28 - Natura, paesaggio e sviluppo del territorio"},
                    {"key": "pab-opere-idrauliche" ,"value": "Ripartizione 30 - Opere idrauliche"},
                    {"key": "pab-libro-fondiario-catasto-fondiario-e-urbano" ,"value": "Ripartizione 41 - Libro fondiario, catasto fondiario e urbano"},
                    {"key": "pab-foreste" ,"value": "Ripartizione 32 - Foreste"},
                    {"key": "comune-merano-urbanistica-ed-edilizia-privata" ,"value": "Ufficio urbanistica ed edilizia privata del comune di Merano"},
                    {"key": "pab-agricoltura" ,"value": "Ripartizione 31 - agricoltura"},
                    {"key": "pab-dipartimento-economia-innovazione-e-europa" ,"value": "Dipartimento Economia, Innovazione e Europa"},
                    {"key": "pab-edilizia-e-servizio-tecnico" ,"value": "Ripartizione 11 - Edilizia e servizio tecnico"},
                    {"key": "pab-beni-culturali" ,"value": "Ripartizione 13 - Beni culturali"},
                    {"key": "pab-economia" ,"value": "Ripartizione 35 - Economia"},
                    {"key": "eurac" ,"value": "Istituto di Telerilevamento Applicato, EURAC"},
                    {"key": "pab-natura-paesaggio-e-sviluppo-del-territorio" ,"value": "Cartografia provinciale e coordinamento geodati - Ripartizione 28"},
                    {"key": "provincia-autonoma-di-bolzano-alto-adige-astat" ,"value": "Istituto Provinciale di Statistica ASTAT"},
                    {"key": "pab-agenzia-provinciale-per-l-ambiente" ,"value": "29. Agenzia provinciale per l'ambiente"}
               ],
               "group_mapping": {
                    "farming": "farming", 
                    "utilitiesCommunication": "boundaries", 
                    "transportation": "boundaries", 
                    "inlandWaters": "environment", 
                    "geoscientificInformation": "geoscientificinformation", 
                    "environment": "environment", 
                    "climatologyMeteorologyAtmosphere": "climatologymeteorologyatmosphere", 
                    "planningCadastre": "boundaries", 
                    "imageryBaseMapsEarthCover": "boundaries", 
                    "elevation": "boundaries", 
                    "boundaries": "boundaries",
                    "structure": "boundaries", 
                    "location": "boundaries", 
                    "economy": "economy",
                    "society": "economy",
                    "biota": "environment",
                    "intelligenceMilitary": "boundaries",
                    "oceans": "environment",
                    "health": "health"
               },
               "ckan_locales_mapping":{
                    "ita": "it",
                    "ger": "de"
               },
               "default_license": "cc-zero"
          }
