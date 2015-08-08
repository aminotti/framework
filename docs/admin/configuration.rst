.. _configuration:

Configuration
=============

They are severals way to set configuration options using this order of priority :

1. Command line argument : ``--my-option=stuff``
2. Environment variable : ``MY_OPTION=stuff``
3. Config file (``conf/config.yaml``) : ``db_uri=stuff``

.. warning::

    * Every options **MUST** exists in config file with a default value in order to be used.
    * Command line arguements overwrites environment variables which overwrites config file.
