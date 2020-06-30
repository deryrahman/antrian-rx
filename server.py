import os
import json
import traceback
from functools import wraps
from flask import Response, request, session, render_template, url_for
from exception import GenericException, AbortException, NotFoundException
from app import app
from user import service as user_service
from recipe import service as recipe_service
custom_exception = [GenericException, AbortException, NotFoundException]


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.errorhandler(GenericException)
def error_handler(error):
    if app.config['DEBUG']:
        traceback.print_exc()
    response = {
        "status": error.status_code,
        "msg": error.message
    }
    return Response(json.dumps(response),
                    status=error.status_code, mimetype='application/json')


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
                error = GenericException(
                    'See trace message for futher info',
                    status_code=e.status_code)
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
    return render_template('index.html')


@app.route('/admin', strict_slashes=False)
def admin():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('admin.html')


@app.route('/api', methods=['GET'], strict_slashes=False)
def api():
    response = ResponseEntity(
        200,
        message="API Antrian Recipe RSUD Cilacap",
        payload={
            'version:': 1.0})
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/users', methods=['POST'], strict_slashes=False)
@exception_helper
@authenticate_helper
def new_user():
    if session['role'] != 'admin':
        raise AbortException('only admin can create user')
    data = request.get_json()
    role = None
    if 'role' in data:
        role = data['role']
    new_user = user_service.create_user(
        name=data['name'],
        email=data['email'],
        role=role,
        password=data['password'])
    response = ResponseEntity(200, payload=new_user.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/users/<email>', methods=['GET'], strict_slashes=False)
@exception_helper
@authenticate_helper
def get_user(email):
    if session['username'] != email:
        raise AbortException('not valid user')
    user = user_service.get_user(email=email)
    response = ResponseEntity(200, payload=user.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/login', methods=['POST'], strict_slashes=False)
@exception_helper
def login():
    data = request.get_json()
    user = user_service.authenticate(
        email=data['email'], password=data['password'])
    if user:
        session['login'] = True
        session['username'] = user.email
        session['role'] = user.role
    response = ResponseEntity(200, payload=user.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/logout', methods=['GET'], strict_slashes=False)
@exception_helper
@authenticate_helper
def logout():
    session.pop('login', None)
    session.pop('username', None)
    session.pop('role', None)
    response = ResponseEntity(200)
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/recipes', methods=['POST'], strict_slashes=False)
@exception_helper
@authenticate_helper
def create_recipe():
    data = request.get_json()
    recipe = recipe_service.create_recipe(
        queue_number=data['queue_number'], user_id=session['username'])
    response = ResponseEntity(200, payload=recipe.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/recipes', methods=['GET'], strict_slashes=False)
@exception_helper
def get_all_recipes():
    recipes = recipe_service.get_all_recipes()
    response = ResponseEntity(200, payload=recipes)
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/recipes/<queue_number>',
           methods=['GET'], strict_slashes=False)
@exception_helper
@authenticate_helper
def get_recipe(queue_number):
    recipe = recipe_service.get_recipe(queue_number)
    response = ResponseEntity(200, payload=recipe.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/recipes/<queue_number>',
           methods=['PUT'], strict_slashes=False)
@exception_helper
@authenticate_helper
def update_recipe(queue_number):
    data = request.get_json()
    recipe = recipe_service.update_recipe(
        queue_number=queue_number,
        status=data['status'],
        user_id=session['username'])
    response = ResponseEntity(200, payload=recipe.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


@app.route('/api/v1/recipes/<queue_number>',
           methods=['DELETE'], strict_slashes=False)
@exception_helper
@authenticate_helper
def delete_recipe(queue_number):
    recipe = recipe_service.delete_recipe(queue_number)
    response = ResponseEntity(200, payload=recipe.to_json())
    return Response(json.dumps(response.to_json()),
                    status=response.status, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
