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

* /etc/uwsgi/apps-available/yamao.ini :

::

    [uwsgi]
    # http = 127.0.0.1:5000  # HTTP standalone
    # socket = 127.0.0.1:8000  # Socket HTTP to talk with nginx (Default socket UNIX)
    stats = 127.0.0.1:9191
    chdir = /path/to/yameo
    # home = /path/to/yameo/venv
    module = main
    callable = application
    processes = 4  # Nb workers
    threads = 4  # Nb cores used


.. note::

    ``processes`` : uwsig is forked in ``<nb>`` process which start differente ``application`` instances.
    ``threads`` : uwsgi run processes in ``<nb>`` thread and move process from thread to thread.

Setup Nginx
+++++++++++

::

    location / { try_files $uri @myapp; }
    
    location @myapp {
        include uwsgi_params;
        #uwsgi_pass      127.0.0.1:8000;
        uwsgi_pass unix:/run/uwsgi/app/myapp/socket;
    }

.. todo::

    Process static files.
