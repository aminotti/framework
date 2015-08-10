from flask import request

from controllers import http
from models import *

http.prefix = "monplug"


@http.route("/country", methods=['POST'])
def country_post():
    return Country.dispatchMethods()


@http.route("/countries", methods=['GET', 'PATCH'])
def countries():
    return Country.dispatchMethods()


@http.route("/country/<int:idcountry>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def country(idcountry):
    return Country.dispatchMethods({'idcountry': idcountry})


@http.route("/country/init")
def country_init():
    Country.createTable()
    return "Create Table Country"
