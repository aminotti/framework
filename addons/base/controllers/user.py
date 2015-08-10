from flask import request

from controllers import http
from models import User

http.prefix = "auth"


# curl -v -X GET -k 'http://localhost:5000/auth/user/aminotti'
@http.route("/user/<uid>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def user(uid):
    return User.dispatchMethods({'uid': uid})
