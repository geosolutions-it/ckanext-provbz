Replace the 'it' and 'de' dirs in the 'ckan/i18n' path with 
the content of this ext dir. 

For each additional changes to the languages files, modify the .po file and then enter:

[root@bolzano src]# cd /usr/lib/ckan/default/src/ckan

[root@bolzano ckan]# . /usr/lib/ckan/default/bin/activate

(default)[root@bolzano ckan]# python setup.py compile_catalog --locale {de or it}

(default)[root@bolzano ckan]systemctl restart supervisord


