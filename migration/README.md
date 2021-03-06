
##PREPARING THE SYSTEM FOR DCAT_AP-IT

This ckanext-provbz has been updated to integrate the old version of this extension with ckanext-dcatapit:

	Follow the steps below only the first time you prepare the system for installing the ckanext-dcatapit.

1. Backup the DB ckan:
	
		su postgres

		pg_dump -U postgres -i ckan > ckan.dump
		
2. Upgrade the python setuptools version installed:

		pip install --upgrade setuptools

3. Install the ckanext-dcat extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src

		git clone https://github.com/ckan/ckanext-dcat.git

		cd ckanext-dcat

		pip install -e .

		pip install -r requirements.txt
		
	- Edit the `/etc/ckan/default/production.ini` adding plugins:
	
		ckan.plugins = dcat dcat_rdf_harvester dcat_json_harvester dcat_json_interface

4. Update the ckanext-multilang extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-multilang

		git pull 

		pip install -e .
		
5. Update the ckanext-provbz extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-provbz

		git pull 

		git checkout dcatapit

		pip install -e .
	
	- Update the `/etc/ckan/default/production.ini` file adding the property below:
	
			ckan.i18n_directory = /usr/lib/ckan/default/src/ckanext-provbz/ckanext/provbz/translations
			
	- Change the name of the `provbz_theme` plugin to `provbz` (you can find that in the `ckan.plugins` property)
	
6. Install the ckanext-dcatapit following the steps reported [here](https://github.com/geosolutions-it/ckanext-dcatapit#installation):

	**Ingore the point number 1**
		
7. Update the ckanext-spatial extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-spatial

		git checkout master

		git pull 

		pip install -e .
		
8. Run the SQL migration script to update DB tables (make sure to have rights to execute the sql file as user postgres):

		su postgres

		psql -U postgres -d ckan -f /usr/lib/ckan/default/src/ckanext-provbz/migration/sql/migration.sql
	
9. Restart CKAN

10. Rebuild the Solr indexes:

		. /usr/lib/ckan/default/bin/activate

		paster --plugin=ckan search-index rebuild  -c /etc/ckan/default/production.ini
