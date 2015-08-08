Set up the environment
======================

Prerequisites
-------------

Python 2.7, pip and some system's libraries must me installed.

GNU/Linux
+++++++++

On Debian like systems :

``apt-get install python-eventlet python-mysqldb libsasl2-dev libjpeg-dev``

For sphinx (about 1Gb require for latexpdf) :

``apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended``


Windows
+++++++

* TODO

Mac OS
++++++

* TODO

Installation
------------

Clone the project.

Database setup
--------------

* TODO

Virtual enviorment
++++++++++++++++++

.. code:: bash

    pip install virtualenv
    cd <project_folder>
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Run the application
-------------------

1. Set debug level in config file :file:`config/config.yaml`.
2. Run ``./main.py``.
3. TODO init DB.

Runing tests
++++++++++++

* Run ``py.test`` for :pep:`8` checks.
* Run ``py.test -m apirest`` to test REST API on database ressources.

Generate doc
++++++++++++

.. code:: bash

    cd <project_folder>/docs
    make html
