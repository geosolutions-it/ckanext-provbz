=============
ckanext-provbz
=============

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

7. Add ``provbz_theme``  and ``provbz_harvester`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN.
