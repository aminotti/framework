from flask import request

from controllers import http
from models import *

http.prefix = "monplug"


@http.route("/room", methods=['POST'])
def room_post():
    return Room.dispatchMethods()


@http.route("/rooms", methods=['PATCH', 'GET', 'DELETE'])
def rooms():
    return Room.dispatchMethods({'name': 'nom'})


@http.route("/room/<int:batiment>/<int:number>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def room(batiment, number):
    return Room.dispatchMethods({'batiment': batiment, 'number': number})


@http.route("/room/init")
def room_init():
    Room.createTable()
    return "Create Table Room"
