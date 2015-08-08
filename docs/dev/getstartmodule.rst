Getting started
===============

A module is used to add features to the core, it can override the core or others modules.

Structure
---------

::

    modules
    └── <mymod>
        ├── __init__.py (empty)
        ├── config.yaml
        ├── settings.yaml
        ├── metadata.py (module's infos)
        ├── locales
        ├── controllers
        │   ├── __init__.py (manual import of module's controllers)
        │   ├── <otherctl>.py (sample controller)
        │   ├── <myctl>.py (a sample controller which add route to an other controller)
        ├── models
        │   ├── __init__.py (manual import of module's models)
        │   ├── <mymodel>.py (sample model)
        └── overrides
            ├── __init__.py (manual import of module's overrides)
            └── <myoverride>.py (model's override sample)

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

Create a route for this module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create file ``modules/<mymod>/controllers/myctl.py`` :

.. code:: python

    from controllers import http

    http.prefix = "mymod"

    @http.route("/user/<email>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    def customer(email):
        return Customer.dispatchMethods({'email': email})

.. note::

    By convention all controllers of the same module **MUST** define the same ``http.prefix``, which relate to the module's name.

2.  Add to ``modules/<mymod>/controllers/__init__.py`` :

.. code:: python

    import myctl

Add new route to another module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example we add a route to ``othermod`` module.

1. Create ``modules/mymod/controllers/otherctl.py`` 

.. warning:: If we use the same controller's filename as in ``othermod`` module, every route defined in the original file will not work.

.. code:: python

    from controllers import http

    http.prefix = "othermod"

    @http.route("/newroute/")
    def newroute():
        return "New route!!"

2. Then add to ``modules/mymod/controllers/__init__.py`` :

.. code:: python

    import othermod

Moving the controller to the core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Move ``modules/mymod/controllers/mymod.py`` to ``controllers/``.
2. Remove import directive in ``modules/mymod/controllers/__init__.py``.

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
