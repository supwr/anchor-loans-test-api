from flask import Flask, request, send_from_directory, render_template, abort
import json
from bson import json_util
from main.controller.users_controller import users
from main.controller.gallery_controller import gallery
from flask_jwt_extended import JWTManager
from main.database import mongo
import os


app = Flask(__name__, template_folder='view')

app.config['JWT_SECRET_KEY'] = 'd53nwH!8KADsu+Rk'
app.config['MONGO_DBNAME'] = 'wedding-gallery'
app.config['MONGO_URI'] = 'mongodb://anchor-loans-mongo/wedding-gallery'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
app.config['ADMIN_ROLE'] = 'ADMIN'
app.config['GUEST_ROLE'] = 'GUEST'

jwt = JWTManager(app)
mongo.init_app(app)


@app.errorhandler(500)
def internal_error(error):
    response = {
        "message": error.description
    }

    return json.dumps(response, default=json_util.default), 500, {'Content-Type': 'application/json; charset=utf-8'}


@app.errorhandler(404)
def not_found(error):
    response = {
        "message": "Page not found"
    }

    return json.dumps(response, default=json_util.default), 404, {'Content-Type': 'application/json; charset=utf-8'}


@app.errorhandler(403)
def forbidden(error):
    response = {
        "message": "You are not allowed to perform this operation"
    }

    return json.dumps(response, default=json_util.default), 403, {'Content-Type': 'application/json; charset=utf-8'}


app.register_blueprint(users, url_prefix='/api/')
app.register_blueprint(gallery, url_prefix='/api/')
