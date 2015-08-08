Working with binary files
=========================

Uploading
---------

1. Create a  :py:class:`~lib.orm.fields.BinaryField` for your model.
2. Use backendFS attribute of :py:class:`~lib.orm.fields.BinaryField` to store on file system (True) or in Database (False).

    .. Warning::

        For ldap backend, :py:class:`~lib.orm.fields.BinaryField` are always store in ldap database.

3. Send your ressource to the API in multipart (json+file) with POST, PUT or PATCH method.

.. note::

    * When file is store to file system, metadata are store in database.
    * When file is store into Database, a extra blob columns is creating : *fieldname*\ _data and *fieldname* contain the metadata.

Downloading
-----------

1. USE GET method on a ressource and you will get the URL of the binary file.

Exemple of PUT resquest
-----------------------

data.bin : ::

    --01ead4a5-7a67-4703-ad02-589886e00923
    Content-Type: application/json; charset=utf-8
    Content-Disposition: form-data; name=ressource

    {"mail": "john@doe.com", "password": "{MD5}wJPI1yL2OsQ2Vj49cReLnQ==", "name": "Doe", "fullname": "John Doe", "title": "CEO", "phone": "+336 11 22 33 44", "smtp": true, "birth": "1972-05-24T23:45+01:00"}
    --01ead4a5-7a67-4703-ad02-589886e00923
    Content-Type: image/jpeg
    Content-Disposition: form-data; name=photo; filename=identity.jpg

    ...image binary content...
    --01ead4a5-7a67-4703-ad02-589886e00923--

CLI : ::

    curl -v -X PUT -H "Content-Type: multipart/form-data; boundary=01ead4a5-7a67-4703-ad02-589886e00923" --data-binary @data.bin 'http://localhost:5000/auth/user/jdoe'

