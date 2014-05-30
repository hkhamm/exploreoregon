This document outlines requirements for the django platform and how they relate to this code bundle.

System Requirements:
- An http server that can load python code. Apache2 + mod_wsgi tested with this build. 
- An sql database server.  Mysql tested with this build.
- The following system packages:
-- 'python-virtualenv', 'gcc', 'python-dev', 'libjpeg-dev', 'zlib1g-dev', 'git-core', 'libmysqlclient-dev', 'python-pip'

Virtualenv:
A virtualenv is required to install all the required python libraries for django.  Follow the below commands to build this projects virtualenv
1. virtualenv --no-site-packages env
2. source /var/www/foobar/env/bin/activate 
3. pip install -U setuptools
4. pip install -U pip
5. ls <full path to provided python_wheel directory>/*.whl $1 | while read x; do pip install --use-wheel --no-index --find-links=<full path to provided python_wheel directory> $x; done
6. ls <full path to provided python_wheel directory>/*.whl $1 | while read x; do pip install --use-wheel --no-index --find-links=<full path to provided python_wheel directory> $x; done
7. The above command is repeated intentionally.  Due to pip having very limited dependancy resolution, the above command must be run twice to ensure all packages install successfully. Dependancy resolution could be done manually, but this is the easiest method to explain and execute.  This should successfully install all the libraries needed inside of the provided wheel directory.

Database:
The following mysqldump is provided with this build to import into the sql database of choice.  Mysql is what this application was build for and tested on.

StaticFiles:
After the virtualenv is built, the code is in place, and the database is imported, collect static needs to be run.
1. Activate the virtualenv.
    - source /var/www/foobar/env/bin/activate 
2. Run the collectstatic manage.py command.
    - /var/www/foobar/code/manage.py collectstatic

===Example config files===
The below config files are created with the following hypthetical setup. The below config files will need to be updated to match your existing environment:
Project Name:                 foobar
Apache User:                  www-data
Path to code dir:             /var/www/foobar/code
Path to Virtualenv:           /var/www/foobar/env
Path to settings_local.py:    /var/www/foobar/code/apps/mainsite/settings_local.py
Path to wsgi.py:              /var/www/foobar/wsgi/wsgi.py
Database User:                foo
Database Name:                bar
Database Password:            ChangeMe
Database Host IP:             127.0.0.1


Apache Virtualhost template file to load django with mod_wsgi enabled:
NOTE: This is not a complete virtualhost file.  This merely outlines key components required to load a python code with mod_wsgi and a wsgi.py config file.
===================================================
<Directory /var/www/foobar/wsgi/wsgi.py>
        Options None
        AllowOverride None
        Order Deny,Allow
        Allow from all
</Directory>

Alias /media/ /var/www/foobar/code/mediafiles/
Alias /static/  /var/www/foobar/code/staticfiles/

WSGIDaemonProcess foobar user=www-data group=www-data processes=3 threads=3 umask=0002
WSGIProcessGroup foobar
WSGIScriptAlias / /var/www/foobar/wsgi/wsgi.py
===================================================



WSGI file example:
===================================================
import sys
import os
import os.path

# code dir is one level above us
APPS_DIR = /var/www/foobar/code

# the env dir is one level above us
ENV_DIR = /var/www/foobar/env

# activate the virtualenv
activate_this = os.path.join(ENV_DIR, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# add the apps directory to the python path
sys.path.insert(0, APPS_DIR)


# load up django 
from django.core.management import execute_manager
from django.core.handlers.wsgi import WSGIHandler

# tell django to find settings at APPS_DIR/mainsite/settings.py'
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings'

# hand off to the wsgi application
application = WSGIHandler()
===================================================



Settings_local.py example:
NOTE: DEBUG = True, DEBUG_ERRORS = True, DEBUG_STATIC = True, TEMPLATE_DEBUG = DEBUG, and DEBUG_MEDIA = True are all very useful for debugging django.
They are very bad for production environments.  Once the site is working set all these values to False.


===================================================
settings_local.py is for all instance specific settings

from settings import *
from mainsite import TOP_DIR

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_ERRORS = True
DEBUG_STATIC = True
DEBUG_MEDIA = True

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bar',                      # Or path to database file if using sqlite3.
        'USER': 'foo',                      # Not used with sqlite3.
        'PASSWORD': 'ChangeMe',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
#            "init_command": "SET storage_engine=InnoDB",  # Uncomment when using MySQL to ensure consistency across servers
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
        'TIMEOUT': 300,
        'KEY_PREFIX': '',
        'VERSION': 1,
    }
}

===================================================
