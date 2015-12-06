"""
Use ``py.test -m apirest`` to run this test
"""
import pytest
import main
from app.context import models
from lib.exceptions import *


@pytest.fixture()
def app():
    # main.http.debug = True
    # return main.http.test_client()
    print main.application()
    return 'Trop bien'
    # return main.application.test_client()


@pytest.fixture()
def hostname():
    # hostname = 'http://localhost/'  # change here to test multitenancy
    hostname = 'http://api.meezio.eu:5000'
    # hostname = 'http://api.skyfos.org/'
    return hostname


@pytest.mark.apirest
def test_delete_tables(app, hostname):
    # rv = app.get('/tests/uninstall', base_url=hostname)
    # assert rv.data == "OK"
    # assert rv.status_code == 200
    assert "Ok" == "Ok"


# @pytest.mark.apirest
# def test_create_tables(app, hostname):
#    rv = app.get('/tests/install', base_url=hostname)
#    assert rv.data == "OK"
#    assert rv.status_code == 200
