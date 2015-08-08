User input security
===================

For every API request, checks are perform automatically on these elements :

* The URL **path**
* The URL's **arguments**
* The body data (**json** and **binary**)

.. note::

    Accepted minetype are :mimetype:`application/json` and :mimetype:`multipart/form-data` (json+file)

Severals point are check :

* The **name** of the fields or argument
* The **type** of the fields or argument
* The **syntax** for string type, using reg expression.
* The minetype, extention and file name (``../../filename`` if forbidden) for binary data

Summarize
---------

+------------+-------------------+-------+--------------------+-----------------+
|            | path              | arg   | data (json fields) | data (binary)   |
+============+===================+=======+====================+=================+
| name       | auto              | [#1]_ | auto               | auto            |
+------------+-------------------+-------+--------------------+-----------------+
| type       | auto              | [#1]_ | auto               | auto            |
+------------+-------------------+-------+--------------------+-----------------+
| str syntax | auto [#2]_        | none  | auto [#2]_         | N/A             |
+------------+-------------------+-------+--------------------+-----------------+

.. [#1] Only for **fields**, **count** and **offset**. Other arguments have to be handled.
.. [#2] For string, default regex protect only against script injection. 

.. important::

    The module developper as to check himself his own URL's **arg** type and name, and set regex for every string type.
