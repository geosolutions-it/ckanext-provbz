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

The ckanext-multilang extension has been developed for CKAN 2.4 or later.

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

8. Restart CKAN.

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
          "group_mapping": {
               "farming": "farming", 
               "utilitiesCommunication": "boundaries", 
               "transportation": "boundaries", 
               "inlandWaters": "environment", 
               "geoscientificInformation": "administration", 
               "environment": "environment", 
               "climatologyMeteorologyAtmosphere": "climatologymeteorologyatmosphere", 
               "planningCadastre": "boundaries", 
               "imageryBaseMapsEarthCover": "boundaries", 
               "elevation": "boundaries", 
               "boundaries": "boundaries"
          },
          "ckan_locales_mapping":{
               "ita": "it",
               "ger": "de"
          },
          "default_license": "cc-zero"
     }
