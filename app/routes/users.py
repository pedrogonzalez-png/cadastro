from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from app import db
from app.models import User


users_bp = Blueprint("users", __name__, url_prefix="/users")


# =========================================================
# CADASTRAR USUÁRIO
# POST /users/
# =========================================================

@users_bp.route("/", methods=["POST"])
def cadastrar_usuario():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Envie os dados em JSON."
        }), 400

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "message": "Nome, email e senha são obrigatórios."
        }), 400

    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente:
        return jsonify({
            "message": "Este email já está cadastrado."
        }), 409

    novo_usuario = User(
        nome=nome,
        email=email
    )

    novo_usuario.definir_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário cadastrado com sucesso!",
        "usuario": {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email
        }
    }), 201


# =========================================================
# LOGIN
# POST /users/login
# =========================================================

@users_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Envie os dados em JSON."
        }), 400

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({
            "message": "Email e senha são obrigatórios."
        }), 400

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({
            "message": "Email ou senha inválidos."
        }), 401

    if not usuario.verificar_senha(senha):
        return jsonify({
            "message": "Email ou senha inválidos."
        }), 401

    access_token = create_access_token(
        identity=str(usuario.id)
    )

    return jsonify({
        "message": "Login realizado com sucesso!",
        "access_token": access_token
    }), 200


# =========================================================
# GET USUÁRIO
# GET /users/<id>
# JWT
# =========================================================

@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def consultar_usuario(id):

    usuario = db.session.get(User, id)

    if not usuario:
        return jsonify({
            "message": "Usuário não encontrado."
        }), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 200


# =========================================================
# PUT USUÁRIO
# PUT /users/<id>
# JWT
# =========================================================

@users_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(id):

    usuario = db.session.get(User, id)

    if not usuario:
        return jsonify({
            "message": "Usuário não encontrado."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Envie os dados em JSON."
        }), 400

    if "nome" in data:
        usuario.nome = data["nome"]

    if "email" in data:

        email_existente = User.query.filter(
            User.email == data["email"],
            User.id != id
        ).first()

        if email_existente:
            return jsonify({
                "message": "Este email já está sendo usado."
            }), 409

        usuario.email = data["email"]

    if "senha" in data:
        usuario.definir_senha(data["senha"])

    db.session.commit()

    return jsonify({
        "message": "Usuário atualizado com sucesso!"
    }), 200


# =========================================================
# DELETE USUÁRIO
# DELETE /users/<id>
# JWT
# =========================================================

@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_usuario(id):

    usuario = db.session.get(User, id)

    if not usuario:
        return jsonify({
            "message": "Usuário não encontrado."
        }), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuário excluído com sucesso!"
    }), 200