"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200

# 1. registrar el usuario // POST
@api.route('/register', methods=['POST'])
def handle_register():
    response_body = {}
    # Aqui va la lógica
    new_user = request.json
    if not new_user:
        response_body['message'] = "Introduce el email y contraseña"
    new_user['email'] = new_user['email'].lower()
    user_a_registrar = User(
        email = new_user['email'],
        password = new_user['password'],
        is_active = True
    )
    db.session.add(user_a_registrar)
    db.session.commit()
    response_body['message'] = "Usuario registrado correctamente"
    return response_body, 201

# 2. logear al usuario -> Le va a dar un token válido // POST
@api.route('/login', methods=['POST'])
def handle_login():
    response_body = {}
    # Aqui la lógica
    user = request.json
    if not user:
        response_body['message'] = "Introduce el email y contraseña"
    user['email'] = user['email'].lower()
    db_user = User.query.filter_by(email=user["email"], password=user["password"]).first()
    if not db_user:
        response_body['message'] = "Usuario no encontrado"
        return response_body, 404
    response_body['message'] = "Usuario logueado correctamente"
    access_token = create_access_token(identity=str(db_user.id)) # Guardamos la identity como string por que si no falla.
    response_body['token'] = access_token
    return response_body, 200

# 3. Check // POST
@api.route('/private', methods=['POST'])
@jwt_required()
def handle_private():
    response_body = {}
    current_user = get_jwt_identity()
    # Devolvemos el valor int al buscar el id en la base de datos
    user = User.query.get(int(current_user))
    if not user:
        response_body['message'] = "Usuario no encontrado"
        return response_body, 404
    response_body['message']='Usuario encontrado!'
    response_body['userInfo'] = user.serialize()
    return response_body, 200
