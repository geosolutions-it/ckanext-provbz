
# ckanext-provbz

The ckanext-provbz CKAN's extension provide some customizations for the CKAN Look and Feel.
In addition this extension provides an harvester that merge functionalities between two other 
harvesters built on the ckanext-spatial extension like:

- https://github.com/geosolutions-it/ckanext-multilang
- https://github.com/geosolutions-it/ckanext-geonetwork

## Requirements

The ckanext-provbz extension has been developed for CKAN 2.4.3 or later.
Other extensions needed as dependencies are:

- https://github.com/geosolutions-it/ckanext-multilang
- https://github.com/geosolutions-it/ckanext-geonetwork
- https://github.com/geosolutions-it/ckanext-pages
- https://github.com/geosolutions-it/ckanext-dcatapit

## Installation

1. Installing all the other extensions required

2. Activate your CKAN virtual environment, for example:

     `. /usr/lib/ckan/default/bin/activate`
     
3. Go into your CKAN path for extension (like /usr/lib/ckan/default/src):

    `git clone https://github.com/geosolutions-it/ckanext-provbz.git`
    
    `cd ckanext-provbz`
    
    `pip install -e .`

4. Add ``provbz``  and ``provbz_harvester`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at ``/etc/ckan/default/production.ini``).

5. (Skip this step for Ckan version >= 2.5) The ckanext-provbz extension provides some updates for the i18n files for 'it' and 'de' languages. Locale files in CKAN (.mo and .po) for these languages must be replaced with files located in this extension at the ckanext-provbz/ckanext/provbz/translations/ path. To do that add the ``ckan.i18n_directory`` configuration property to the production.ini file as follow:

	`ckan.i18n_directory = $BASE_PATH/ckanext-provbz/ckanext/provbz/translations`

6. Update the production.ini configuration finding the default property ``licenses_group_url`` and change the value:

         licenses_group_url = file:///usr/lib/ckan/default/src/ckanext-provbz/ckanext/provbz/licenses/ckan.json

7. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     `sudo service apache2 reload`

## Development Installation

To install `ckanext-provbz` for development, activate your CKAN virtualenv and do:

	git clone https://github.com/geosolutions-it/ckanext-provbz.git

	cd ckanext-provbz

	python setup.py develop

	pip install -r dev-requirements.txt

## Harvest Configuration

Using the ckanext-provbz harvester you can use an additional configuration property in addition to the other allowed for the ckanext-geonetwork and ckanext-multilang harvesters:

* ``default_license``: with this property you can specify the default license to use for the CKAN's dataset if none useLimitation has been found into the metadata. Below an example:

        {
            "default_license": "cc-zero"
        }
	
* ``default_values``: with this property you can specify some default values to use for missing properties in CSW metadata. Default values are defined into the harvester but can be overridden in the CKAN harvest source json configuration. Below the predefined defaults:

		{
			'dataset_theme': 'OP_DATPRO',
			'dataset_place': 'ITA_BZO',
			'dataset_language': '{ITA,DEU}',
			'agent_code': 'p_bz',
			'frequency': 'UNKNOWN',
			'agent_code_regex': {
			    'regex': '\(([^)]+)\:([^)]+)\)',
			    'groups': [2] # optional, dependes by the regular expression
			},
			'org_name_regex': {
			    'regex': '([^(]*)(\(IPa[^)]*\))(.+)',
			    'groups': [1,3] # optional, dependes by the regular expression
			},
			'dcatapit_skos_theme_id': 'theme.data-theme-skos',
			'dcatapit_skos_places_id': 'theme.places-skos'
		}
	
	**note**:
		the **agent_code_regex** and **org_name_regex** (regex and/or group properties) must be changed if the corresponding 'organizationName'
		value change in the CSW metadata. Current default value has been set to match a string type like the following:

		Provincia Autonoma di Bolzano (IPa: p_bz) - Ripartizione 28 - Natura, paesaggio e sviluppo del territorio
		
	where the **agent_code_regex** match the IPa code **p_bz** and the **org_name_regex** match the organization name
	value **Provincia Autonoma di Bolzano - Ripartizione 28 - Natura, paesaggio e sviluppo del territorio**.
	
	the **dcatapit_skos_theme_id** and **dcatapit_skos_places_id** values correspond to the thesaurus identifiers speficied in the CSW metadata (related to the eu_theme.rdf and places.rdf themes) so if the metadata values change also these configuration options must be modified accordingly. 

Below the complete configuration to use:

        {
			"private_datasets": "False", 
			"version": "2.6", 
			"harvest_iso_categories": "True",
			"default_extras": {
				"geocat_layer_url": "http://geocatalogo.retecivica.bz.it/geokatalog/#!home&layer="
			},
			"organisation_mapping": [
				{
					"key": "pab-foreste",
					"value": "Ufficio 32.3 - Ufficio Pianificazione forestale",
					"value_it":"PAB: Rip. Foreste",
					"value_de":"APB: Abt. Frostwirtschaft"
				},
				{
					"key": "pab-foreste",
					"value": "Ufficio 32.4 - Ufficio Caccia e pesca",
					"value_it":"PAB: Rip. Foreste",
					"value_de":"APB: Abt. Frostwirtschaft"
				},
				{
					"key": "comune-bolzano-sistema-informativo-territoriale",
					"value": "Ufficio Sistema Informativo Territoriale, Comune di Bolzano",
					"value_it":"Comune Bolzano",
					"value_de":"Gemeinde Bozen"
				},
				{
					"key": "pab-agenzia-provinciale-per-l-ambiente",
					"value": "Ripartizione 29 - Agenzia provinciale per l'ambiente",
					"value_it":"PAB: Agenzia per l´ambiente",
					"value_de":"APB: Agentur für Umwelt"
				},
				{
					"key": "pab-servizio-strade",
					"value": "Ripartizione 12 - Servizio Strade",
					"value_it":"PAB: Rip. Servizio strade",
					"value_de":"APB: Abt. Straßendienst"
				},
				{
					"key": "pab-servizio-strade",
					"value": "Ripartizione 12 - Servizio strade",
					"value_it":"PAB: Rip. Servizio strade",
					"value_de":"APB: Abt. Straßendienst"
				},
				{
					"key": "pab-protezione-antincendi-e-civile",
					"value": "Ripartizione 26 - Protezione antincendi e civile",
					"value_it":"Agenzia per la protezione civile",
					"value_de":"Agentur für Bevölkerungsschutz"
				},
				{
					"key": "pab-protezione-antincendi-e-civile",
					"value": "Ripartizione 26 - protezione antincendi e civile",
					"value_it":"Agenzia per la protezione civile",
					"value_de":"Agentur für Bevölkerungsschutz"
				},
				{
					"key": "pab-protezione-antincendi-e-civile",
					"value": "Abteilung 26 - Brand- und Zivilschutz",
					"value_it":"Agenzia per la protezione civile",
					"value_de":"Agentur für Bevölkerungsschutz"
				},
				{
					"key": "pab-natura-paesaggio-e-sviluppo-del-territorio",
					"value": "Ripartizione 28 - Natura, paesaggio e sviluppo del territorio",
					"value_it":"PAB: Rip. Natura, paesaggio e sviluppo del territorio",
					"value_de":"APB: Abt. Natur, Landschaft und Raumentwicklung"
				},
				{
					"key": "pab-protezione-antincendi-e-civile",
					"value": "Ripartizione 30 - Opere idrauliche",
					"value_it":"Agenzia per la protezione civile",
					"value_de":"Agentur für Bevölkerungsschutz"
				},
				{
					"key": "pab-libro-fondiario-catasto-fondiario-e-urbano",
					"value": "Ripartizione 41 - Libro fondiario, catasto fondiario e urbano",
					"value_it":"PAB: Rip.  Libro fondiario e Catasto",
					"value_de":"APB: Abt.  Grundbuch und Kataster"
				},
				{
					"key": "pab-foreste",
					"value": "Ripartizione 32 - Foreste",
					"value_it":"PAB: Rip. Foreste",
					"value_de":"APB: Abt. Frostwirtschaft"
				},
				{
					"key": "comune-merano-urbanistica-ed-edilizia-privata",
					"value": "Ufficio urbanistica ed edilizia privata del comune di Merano",
					"value_it":"Comune Merano",
					"value_de":"Gemenide Meran"
				},
				{
					"key": "pab-agricoltura",
					"value": "Ripartizione 31 - agricoltura",
					"value_it":"PAB: Rip. Agricoltura",
					"value_de":"APB: Abt. Landwitschaft"
				},
				{
					"key": "pab-agricoltura",
					"value": "Ripartizione 31 - Agricoltura",
					"value_it":"PAB: Rip. Agricoltura",
					"value_de":"APB: Abt. Landwitschaft"
				},
				{
					"key": "pab-dipartimento-economia-innovazione-e-europa",
					"value": "Dipartimento Economia, Innovazione e Europa",
					"value_it":"Dip. economia, innovazione e Europa",
					"value_de":"Ressort Wirtschaft, Innovation und Europa"
				},
				{
					"key": "pab-edilizia-e-servizio-tecnico",
					"value": "Ripartizione 11 - Edilizia e servizio tecnico",
					"value_it":"PAB: Rip.  Edilizia",
					"value_de":"APB: Abt.  Hochbau"
				},
						{
					"key": "pab-edilizia-e-servizio-tecnico",
					"value": "Abteilung 11 - Hochbau und technischer Dienst",
					"value_it":"PAB: Rip.  Edilizia",
					"value_de":"APB: Abt.  Hochbau"
				},
				{
					"key": "pab-beni-culturali",
					"value": "Ripartizione 13 - Beni culturali",
					"value_it":"PAB: Rip. Beni culturali",
					"value_de":"APB: Abt. Denkmalpflege"
				},
				{
					"key": "pab-economia",
					"value": "Ripartizione 35 - Economia",
					"value_it":"PAB: Rip. Economia",
					"value_de":"APB: Abt. Wirtschaft"
				},
				{
					"key": "eurac",
					"value": "Istituto di Telerilevamento Applicato, EURAC",
					"value_it":"EURAC research",
					"value_de":"EURAC research"
				},
						{
					"key": "ras",
					"value": "RAS - Radiotelevisione Azienda Speciale",
					"value_it":"RAS",
					"value_de":"RAS"
				},
				{
					"key": "pab-natura-paesaggio-e-sviluppo-del-territorio",
					"value": "Cartografia provinciale e coordinamento geodati - Ripartizione 28",
					"value_it":"PAB: Rip. Natura, paesaggio e sviluppo del territorio",
					"value_de":"APB: Abt. Natur, Landschaft und Raumentwicklung"
				},
				{
					"key": "provincia-autonoma-di-bolzano-alto-adige-astat",
					"value": "Istituto Provinciale di Statistica ASTAT",
					"value_it":"PAB: Uff. Statistica (ASTAT)",
					"value_de":"APB: Amt für Statistik (ASTAT)"
				},
				{
					"key": "pab-agenzia-provinciale-per-l-ambiente",
					"value": "29. Agenzia provinciale per l'ambiente",
					"value_it":"PAB: Agenzia per l´ambiente",
					"value_de":"APB: Agentur für Umwelt"
				}
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

## Managing translations

The provbz extension implements the ITranslation CKAN's interface so the translations procedure of the GUI elements is automatically covered using the translations files provided in the i18n directory. 

### Creating a new translation
To create a new translation proceed as follow:

1. Extract new messages from your extension updating the pot file:

     `python setup.py extract_messages`
     
2.  Create a translation file for your language (a po file) using the existing pot file in this plugin:

     `python setup.py init_catalog --locale YOUR_LANGUAGE`

     Replace YOUR_LANGUAGE with the two-letter ISO language code (e.g. es, de).
     
3. Do the translation into the po file

4. Once the translation files (po) have been updated, either manually or via Transifex, compile them by running:

     `python setup.py compile_catalog --locale YOUR_LANGUAGE`
     
### Updating an existing translation
In order to update the existing translations proceed as follow:

1. Extract new messages from your extension updating the pot file:

     `python setup.py extract_messages`
     
2. Update the strings in your po file, while preserving your po edits, by doing:

     `python setup.py update_catalog --locale YOUR-LANGUAGE`

3. Once the translation files (po) have been updated adding the new translations needed, compile them by running:

     `python setup.py compile_catalog --locale YOUR_LANGUAGE`
