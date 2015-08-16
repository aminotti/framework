Getting started
===============

A module is used to add features or extend the core, it can override the cores module or extras modules.

Structure
---------

::

    modules
    └── <mymod>
        ├── __init__.py (manual import of module's controllers)
        ├── config.yaml
        ├── settings.yaml
        ├── metadata.py (module's infos)
        ├── locales
        ├── controllers
        │   ├── __init__.py (empty)
        │   ├── <myctl>.py (standalone controller)
        ├── models
        │   ├── __init__.py (manual import of module's models)
        │   ├── <mymodel>.py (sample model)
        └── overrides
            ├── __init__.py (manual import of module's overrides)
            └── <myoverride>.py (model's override sample)

.. note::

    Here **modules** is a directory define with ``--module-path`` argument.

Configuration
-------------

Default configuration for the module is set  in ``modules/<mymod>/config.yaml``. It can be override by environment variable or command line arguments, see :ref:`configuration`.

Settings for the module are set in ``modules/<mymod>/settings.yaml``.

config.yaml
~~~~~~~~~~~

Global plugin's configuration, common for all tenants.

Example :

.. code:: yaml

    language: DE_de
    maxSize: 100
    db_uri: mysql://root@127.0.0.1/mydbname

When we move a module to the core, the ``config/config.yaml`` **MUST** be like this :

.. code:: yaml

    mymod:
        language: DE_de
        maxSize: 100
        db_uri: mysql://root@127.0.0.1/mydbname

settings.yaml
~~~~~~~~~~~~~

This file contain a description of the settings and their defaults values.
These informations are use to build the UI.
We can edit and store them in DB (and overwrite them by user preferences).

.. code:: yaml

    website:
        label: Web site URL
        defaultValue: http://localhost/
        type: url
        regex: ~

    color:
        label: Main color
        defaultValue: #4576FF
        type: color
        regex: ~

When we move a module to the core, the ``config/settings.yaml`` **MUST** be like this :

.. code:: yaml

    mymod:
        website:
            label: Web site URL
            defaultValue: http://localhost/
            type: url
            regex: ~

        color:
            label: Main color
            defaultValue: #4576FF
            type: color
            regex: ~

Using
~~~~~

.. code:: python

    from config import conf

    print dir(conf)

    conf.mymodLanguage
    conf.mymodMaxsize
    conf.mymodDb_uri
    conf.mymodWebsite
    conf.mymodColor

Metadata
--------

Writting
~~~~~~~~~~

* Create ``<mymod>/metadata.py`` file :

.. code:: python

    # -*- coding: utf-8 -*-

    infos = {
        'name': "Module's fullname",
        'version': '1.0',
        'description': """
        Description text
        """,
        'author': "Author Name",
        'email': "author@name.tld",
        'website': "http://www.monplug.tld",
        'git': "https://git.name.tld/monplug.git",
        'license': "AGPL-3",
    }

Using
~~~~~

.. code:: python

    from modules.metadata import modules_infos

    # list of dictionnaries
    print modules_infos

    for infos in modules_infos:
        print infos["name"]

Route/controllers
-----------------

They is 2 ways to add routes, you can add routes to a model or you can add standalone routes.

Standalone routes
~~~~~~~~~~~~~~~~~

1. Create file ``modules/<mymod>/controllers/myctl.py`` :


.. code:: python

    from flask import current_app
    from app.controller import Controller


    ctl = Controller()

    @ctl.route('/show/')
    def show_tenant():
        return current_app.tenant

    @ctl.route('/hello/')
    def hello():
        return 'Hello world!'

.. note::

    This exemple show how to access tenancy prefix using Flask current_app where it is stored.

2.  Add to ``modules/<mymod>/__init__.py`` :

.. code:: python

    from myctl import ctl

Add route to a model
~~~~~~~~~~~~~~~~~~~~

See **Model** below.

Model
-----

.. note:: See :doc:`libsql` and :doc:`libldap` for more details.

Create a model
~~~~~~~~~~~~~~~~~~~~~~

1. Create file ``modules/mymod/models/mymodel.py`` :

.. code:: python

    from lib.orm import *
    from app import HTTPMethod

    class mymodel(HTTPMethod, SQLTable):
        email = EmailField(primaryKey=True)
        firstname = StringField(length=255)
        lastname = StringField(length=255)
        telephone = TelField()

2. Add to file ``modules/mymod/models/__init__.py`` :

.. code:: python

    from .mymodel import mymodel

Alter another module's model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Valable également pour overrrider d'autres classes que les models.

1. Create file  ``modules/mymod/overrides/myoverride.py`` :

.. code:: python

    from lib.orm import *
    from models import Country

    def new_method(self, value):
        return value

    def other_method():
        return "My other method"

    Country.test1 = new_method
    Country.test2 = staticmethod(other_method)
    Country.planet = "Earth"
    Country.addField('tld', StringField(unique=True, length=4))

2. Add to file ``modules/mymod/overrides/__init__.py`` :

.. code:: python

    import myoverride

.. note:: This method work too with other classes than models.

Moving the model to the core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Move ``modules/mymod/models/mymodel.py`` to ``models/``.
2. Cut and paste ``from .mymodel import mymodel`` from ``modules/mymod/models/__init__.py`` to ``models/__init__.py``.

Adding logic to your model
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from lib.orm import *
    from app import HTTPMethod

    class mymodel(HTTPMethod, SQLTable):
        email = EmailField(primaryKey=True)
        firstname = StringField(length=255)
        lastname = StringField(length=255)
        fullname = StringField(length=500)
        telephone = TelField()

        @property
        def fullname(self):
            return self._fullname

        @price.setter
        def fullname(self, value):
                self._fullname = "{} {}".format(firstname, lastname)
