
##PREPARING THE SYSTEM FOR DCAT_AP-IT

This ckanext-provbz has been updated to integrate the old version of this extension with ckanext-dcatapit:

	Follow the steps below only the first time you prepare the system for installing the ckanext-dcatapit.

1. Backup the DB ckan:
	
		su postgres

		pg_dump -U postgres -i ckan > ckan.dump
	
2. Run the SQL migration script to update DB tables:

		su postgres

		psql -U postgres -d ckan -f /usr/lib/ckan/default/src/ckanext-provbz/migration/sql/migration.sql
	
3. Upgrade the python setuptools version installed (only if ckan version < 2.5):

		pip install --upgrade setuptools

4. Install the ckanext-dcat extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src

		git clone https://github.com/ckan/ckanext-dcat.git

		cd ckanext-dcat

		pip install -e .

		pip install -r requirements.txt

5. Install the ckanext-dcatapit following the steps reported [here](https://github.com/geosolutions-it/ckanext-dcatapit#installation):

	**Ingore the point number 1**
	
6. Update the ckanext-multilang extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-multilang

		git pull 

		pip install -e .
	
7. Update the ckanext-provbz extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-provbz

		git pull 

		git checkout dcatapit

		pip install -e .
	
	- Update the `/etc/ckan/default/production.ini` file adding the property below:
	
			ckan.i18n_directory = /usr/lib/ckan/default/src/ckanext-provbz/ckanext/provbz/translations
			
	- Change the name of the `provbz_theme` plugin to `provbz` (you can find that in the `ckan.plugins` property)
		
8. Update the ckanext-spatial extension:

		. /usr/lib/ckan/default/bin/activate

		cd /usr/lib/ckan/default/src/ckanext-spatial

		git checkout master

		git pull 

		pip install -e .
	
9. Restart CKAN

10. Rebuild the Solr indexes:

		. /usr/lib/ckan/default/bin/activate

		paster --plugin=ckan search-index rebuild  -c /etc/ckan/default/production.ini
