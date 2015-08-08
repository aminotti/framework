ORM SQL
+++++++

Class SQLTable
==============

.. autoclass:: lib.orm.sql.sqlobjects.SQLTable
    :noindex:

Field objects
==============

.. automodule:: lib.orm.fields
    :no-members:
    :noindex:

SQLFilter object
================

.. note::

    See :py:mod:`~lib.orm.filter` for generic ORM filters.

.. autoclass:: lib.orm.sql.sqlobjects.SQLFilter
    :noindex:

Relation 1 to many
==================

.. autoclass:: lib.orm.sql.sqlobjects.ForeignKey
    :noindex:

Relation many to many
=====================

URI scheme
----------

 * Managing A ressource : ``/a_ressource/[<ida>]`` (CRUD on A ressource)
 * Managing B ressource : ``/b_ressource/[<idb>]`` (CRUD on B ressource)
 * Managing A/B relation : ``/a_ressource/<ida>/b_ressource/<idb>`` (CRUD on A/B relation)
 * Listing B ressources of A : ``/a_ressource/<ida>/b_ressources`` (Read relation A/B)

.. code:: python

    @http.route("/a_ressource/<ida>/b_ressources", methods=['GET'])
    def relab(ida):
        if request.method == 'GET':
            return RelAB.getHTTP({'ida': ida}, fields=request.args.getlist('fields'), relationship='ressourceB')

Implementation
--------------

.. code:: python

    from lib.orm.sql import *


    class RelationAB(SQLRelationship):
        ressourceA = ForeignKey('RessourceA', primaryKey=True)
        ressourceB = ForeignKey('RessourceB', primaryKey=True)
        dtRelation = DateCol()

Class SQLRelationship
---------------------

.. autoclass:: lib.orm.sql.sqlobjects.SQLRelationship
    :noindex:

Class SQLView
=============

.. autoclass:: lib.orm.sql.sqlobjects.SQLView
    :noindex:

Example :

.. code:: python

    from lib.orm.sql import *
    from app import HTTPMethod
    from config import conf


    class Booking(HTTPMethod, SQLView):
        uri = conf.sample_moduleDb_uri

        nom = StringCol(colName='fullname')
        batiment = IntCol()
        email = email = EmailCol()
        reservation = DateCol()
        name = StringCol(colName='room_name')

.. note::

    Don"t need more specification for columns because it's only use to SELECT (get method).

Annexes
=======

.. todo::

    Améliorer SQLView en gérant la creation de la vue.

    .. code:: sql

        CREATE VIEW booking AS (
        SELECT fullname, batiment, email, reservation, room_name FROM customer 
        INNER JOIN relcustroom USING(email) 
        INNER JOIN batman.room USING(number, batiment));
