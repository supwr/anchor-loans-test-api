from flask import Blueprint, render_template, jsonify, request, abort, current_app as app
import json
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from main.service.gallery_service import GalleryService
from main.service.users_service import UsersService
import os
from main.auth import admin_required


gallery = Blueprint('gallery', __name__)


@gallery.route('/gallery', methods=['GET'])
@jwt_optional
def index():
    try:
        current_user = UsersService.get_user_by_username(get_jwt_identity())

        if current_user is None or current_user["role"] == app.config['GUEST_ROLE']:
            images = list(GalleryService.list_approved_images())
        else:
            images = list(GalleryService.list_all_images())

        return json.dumps(images, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@gallery.route('/gallery/upload', methods=['POST'])
@jwt_required
def upload():
    try:

        current_user = UsersService.get_user_by_username(get_jwt_identity())

        if 'file' not in request.files:
            response = jsonify({"message": "Adicione um arquivo."})
            response.status_code = 400
            return response

        file = request.files['file']

        if file.filename == '':
            response = jsonify({"message": "Adicione um arquivo."})
            response.status_code = 400
            return response

        if file is None:
            abort(500)

        image = GalleryService.get_image_by_id(GalleryService.new_image(file, current_user["_id"]))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@gallery.route('/gallery/<id>', methods=['DELETE'])
@jwt_required
def remove_image(id):
    try:
        current_user = UsersService.get_user_by_username(get_jwt_identity())
        image = GalleryService.get_image_by_id(ObjectId(id))

        if image is None:
            return json.dumps([], default=json_util.default), 204, {'Content-Type': 'application/json; charset=utf-8'}

        GalleryService.remove_image(image)

        return json.dumps([], default=json_util.default), 204, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@gallery.route('/gallery/<id>/approve', methods=['PUT'])
@jwt_required
@admin_required
def approve_image(id):
    try:
        current_user = UsersService.get_user_by_username(get_jwt_identity())

        GalleryService.approve_image(current_user["_id"], ObjectId(id))

        image = GalleryService.get_image_by_id(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@gallery.route('/gallery/<id>/disapprove', methods=['PUT'])
@jwt_required
@admin_required
def disapprove_image(id):
    try:
        current_user = UsersService.get_user_by_username(get_jwt_identity())

        GalleryService.disapprove_image(current_user["_id"], ObjectId(id))

        image = GalleryService.get_image_by_id(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@gallery.route('/gallery/<id>/like', methods=['PUT'])
@jwt_required
def like_image(id):
    try:
        current_user = UsersService.get_user_by_username(get_jwt_identity())

        GalleryService.like_image(current_user["_id"], ObjectId(id))

        image = GalleryService.get_image_by_id(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)
