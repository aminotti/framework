Writing REST API
================

HTTP methods
------------

CRUD
~~~~

* POST = **Create** (internal managment of indentifier)
* PUT = **Create** (identifier provided) or full **update**
* GET = **Read**
* PATCH = **Update** (partial)
* DELETE = **Delete**

Type of methods
~~~~~~~~~~~~~~~

* Idempotent : Same behavior for every resquest on the resource 
* Safe : don't alter the ressource

+---------------+--------------+--------+
| HTTP Method   | Idempotent   | Safe   |
+===============+==============+========+
| OPTIONS       | yes          | yes    |
+---------------+--------------+--------+
| GET           | yes          | yes    |
+---------------+--------------+--------+
| HEAD          | yes          | yes    |
+---------------+--------------+--------+
| PUT           | yes          | no     |
+---------------+--------------+--------+
| DELETE        | yes          | no     |
+---------------+--------------+--------+
| POST          | no           | no     |
+---------------+--------------+--------+
| PATCH         | no           | no     |
+---------------+--------------+--------+

Return codes
------------

* 200 - OK ( **GET** Everything worked)
* 201 - Created ( **POST** : response body or header *Location* contains created ressource URI)
* 204 - No Content ( **PUT**, **DELETE**, **PATCH** request processed    successfully but no response body is needed)
* 400 - Bad Request (bad request parameter's)
* 401 - Unauthorized (require authentification)
* 403 - Forbidden (authenticated user not allow to access this ressource)
* 404 - Not Found ( **GET**. Ressource not found or bad URI)
* 409 - Conflict (Try to create ressource with existing identifier, not use because *PUT* with an id is an *update*)
* 500 - Internal Server Error (The API did something wrong)

.. tip::

    Use :py:mod:`lib.exceptions` module to raise appropriate errors.
