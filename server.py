from flask import Response, request, session
import json
from exception import GenericException, AbortException, NotFoundException
from config import app
import traceback
from functools import wraps
from user import service as user_service
custom_exception = [GenericException, AbortException, NotFoundException]


@app.errorhandler(GenericException)
def error_handler(error):
    if app.config['DEBUG']:
        traceback.print_exc()
    response = {
        "status": error.status_code,
        "msg": error.message
    }
    return Response(json.dumps(response), status=error.status_code, mimetype='application/json')


def authenticate_helper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' in session and session['login']:
            response = f(*args, **kwargs)
            return response
        raise AbortException('not login')
    return decorated_function


def exception_helper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            return response
        except Exception as e:
            if type(e) in custom_exception:
                return error_handler(e)
            error = GenericException('See trace message for futher info')
            if(hasattr(e, 'status_code')):
                error = GenericException('See trace message for futher info', status_code=e.status_code)
            return error_handler(error)
    return decorated_function


class ResponseEntity():
    def __init__(self, status, message=None, payload=None):
        self.status = status
        self.message = message
        self.payload = payload

    def to_json(self):
        return self.__dict__


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    response = ResponseEntity(200, message="bum", payload=[1, 2, 3])
    return Response(json.dumps(response.to_json()), status=response.status, mimetype='application/json')


@app.route('/users', methods=['POST'], strict_slashes=False)
@exception_helper
@authenticate_helper
def new_user():
    if session['role'] != 'admin':
        raise AbortException('only admin can create user')
    data = request.get_json()
    role = None
    if 'role' in data:
        role = data['role']
    new_user = user_service.create_user(name=data['name'], email=data['email'], role=role, password=data['password'])
    response = ResponseEntity(200, payload=new_user.to_json())
    return Response(json.dumps(response.to_json()), status=response.status, mimetype='application/json')


@app.route('/users/<email>', methods=['GET'], strict_slashes=False)
@exception_helper
@authenticate_helper
def get_user(email):
    print(session['username'])
    print(email)
    if session['username'] != email:
        raise AbortException('not valid user')
    user = user_service.get_user(email=email)
    response = ResponseEntity(200, payload=user.to_json())
    return Response(json.dumps(response.to_json()), status=response.status, mimetype='application/json')


@app.route('/login', methods=['POST'], strict_slashes=False)
@exception_helper
def login():
    data = request.get_json()
    user = user_service.authenticate(email=data['email'], password=data['password'])
    if user:
        session['login'] = True
        session['username'] = user.email
        session['role'] = user.role
    response = ResponseEntity(200, payload=user.to_json())
    return Response(json.dumps(response.to_json()), status=response.status, mimetype='application/json')


@app.route('/logout', methods=['GET'], strict_slashes=False)
@exception_helper
@authenticate_helper
def logout():
    session['login'] = False
    response = ResponseEntity(200)
    return Response(json.dumps(response.to_json()), status=response.status, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
