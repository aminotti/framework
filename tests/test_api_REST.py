"""
Use ``py.test -m apirest`` to run this test
"""
import pytest
import json
import urllib2


@pytest.fixture()
def hostname():
    hostname = 'http://api.meezio.eu:5000/'
    return hostname


@pytest.mark.apirest
@pytest.mark.all
def test_add_new_rooms(hostname):
    url = "{}{}".format(hostname, "room/")

    request = urllib2.Request(url, json.dumps({'batiment': 1, 'numero': 1, 'nom': 'My Room'}), {'Content-Type': 'application/json'})
    response = urllib2.urlopen(request)
    assert response.getcode() == 201
    response.close()

    try:
        request = urllib2.Request(url, json.dumps({'batiment': 1, 'numero': 2, 'name': 'My Failed Room'}), {'Content-Type': 'application/json'})
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        assert error.getcode() == 400
        assert error.read() == """{\n  "msg": "Bad attribute : 'name'"\n}"""
        response.close()

    with open("tests/room.bin") as f:
        data = f.read()
        request3 = urllib2.Request(url, data, {'Content-Type': 'multipart/form-data; boundary=01ead4a5-7a67-4703-ad02-589886e00923'})
        response3 = urllib2.urlopen(request3)
        assert response3.getcode() == 201
        response3.close()


@pytest.mark.apirest
@pytest.mark.all
def test_update_a_room(hostname):
    url = "{}{}".format(hostname, "room/1/1/")

    request = urllib2.Request(url, json.dumps({'nom': 'My updated Room'}), {'Content-Type': 'application/json'})
    request.get_method = lambda: 'PATCH'
    response = urllib2.urlopen(request)
    assert response.getcode() == 204
    response.close()


@pytest.mark.apirest
@pytest.mark.all
def test_get_a_room(hostname):
    url = "{}{}".format(hostname, "room/1/1/")

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    assert response.read() == """{"batiment": 1, "contrat": null, "minibar": false, "nom": "My updated Room", "numero": 1, "ready": "14:45", "score": 3.14}"""
    assert response.getcode() == 200
    response.close()


@pytest.mark.apirest
@pytest.mark.all
def test_delete_a_room(hostname):
    url = "{}{}".format(hostname, "room/1/1/")

    request = urllib2.Request(url)
    request.get_method = lambda: 'DELETE'
    response = urllib2.urlopen(request)
    assert response.getcode() == 204
    response.close()


"""
    with open("tests/france.bin") as f:
        data = f.read()
    content_type = 'multipart/form-data; boundary=01ead4a5-7a67-4703-ad02-589886e00923'
    rv = app.post('/monplug/country', data=data, content_type=content_type, base_url=hostname)
    assert rv.status_code == 201

"""
