from flask import request

from controllers import http
from models import *

http.prefix = "monplug"


@http.route("/customer/<email>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def customer(email):
    return Customer.dispatchMethods({'email': email})


@http.route("/customer/<email>/room/<int:batiment>/<int:number>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def custroom(email, batiment, number):
    return RelCustRoom.dispatchMethods({'email': email, 'batiment': batiment, 'number': number})


@http.route("/customer/<email>/rooms", methods=['GET'])
def custrooms(email):
    return RelCustRoom.dispatchMethods({'email': email}, relationship='room')


@http.route("/customer/<email>/bookings", methods=['GET'])
def bookings(email):
    return Booking.dispatchMethods({'email': email}, relationship='room')


@http.route("/customer/init")
def customer_init():
    Customer.createTable()
    RelCustRoom.createTable()
    return "Create Table Customer"
