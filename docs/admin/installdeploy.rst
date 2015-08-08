Installation and deployement
============================

Installation
^^^^^^^^^^^^

.. todo::

    * install OS dependancies (debian package)
    * install app (git clone)
    * install python dependencie (requirements.txt)

Deployement
^^^^^^^^^^^

This deployement is done on Debian like distribution using uwsgi and nginx.

Install package
+++++++++++++++

``apt-get install nginx uwsgi uwsgi-extra uwsgi-plugin-python``

Setup uwsgi
+++++++++++

* /etc/uwsgi/apps-available/myapp.ini :

::

    [uwsgi]
    # http = 127.0.0.1:5000  # HTTP standalone
    # socket = 127.0.0.1:8000  # Socket HTTP to talk with nginx (Default socket UNIX)
    stats = 127.0.0.1:9191
    chdir = /path/to/core-backend
    home = /path/to/core-backend/venv
    module = main
    callable = http
    processes = 4  # Nb workers
    threads = 2  # Nb cores used

Setup Nginx
+++++++++++

::

    location / { try_files $uri @myapp; }
    
    location @myapp {
        include uwsgi_params;
        #uwsgi_pass      127.0.0.1:8000;
        uwsgi_pass unix:/run/uwsgi/app/myapp/socket;
    }
