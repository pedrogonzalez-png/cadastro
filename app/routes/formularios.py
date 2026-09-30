from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Formulario


formularios_bp = Blueprint(
    "formularios",
    __name__,
    url_prefix="/formularios"
)


# =========================================================
# CADASTRAR FORMULÁRIO
# POST /formularios/
# JWT
# =========================================================

@formularios_bp.route("/", methods=["POST"])
@jwt_required()
def cadastrar_formulario():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Envie os dados em JSON."
        }), 400

    titulo = data.get("titulo")
    descricao = data.get("descricao")

    if not titulo or not descricao:
        return jsonify({
            "message": "Título e descrição são obrigatórios."
        }), 400

    usuario_id = int(get_jwt_identity())

    novo_formulario = Formulario(
        titulo=titulo,
        descricao=descricao,
        usuario_id=usuario_id
    )

    db.session.add(novo_formulario)
    db.session.commit()

    return jsonify({
        "message": "Formulário cadastrado com sucesso!",
        "formulario": {
            "id": novo_formulario.id,
            "titulo": novo_formulario.titulo,
            "descricao": novo_formulario.descricao,
            "usuario_id": novo_formulario.usuario_id
        }
    }), 201


# =========================================================
# GET FORMULÁRIO
# GET /formularios/<id>
# JWT
# =========================================================

@formularios_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def consultar_formulario(id):

    formulario = db.session.get(Formulario, id)

    if not formulario:
        return jsonify({
            "message": "Formulário não encontrado."
        }), 404

    return jsonify({
        "id": formulario.id,
        "titulo": formulario.titulo,
        "descricao": formulario.descricao,
        "usuario_id": formulario.usuario_id
    }), 200


# =========================================================
# PUT FORMULÁRIO
# PUT /formularios/<id>
# JWT
# =========================================================

@formularios_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_formulario(id):

    formulario = db.session.get(Formulario, id)

    if not formulario:
        return jsonify({
            "message": "Formulário não encontrado."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Envie os dados em JSON."
        }), 400

    if "titulo" in data:
        formulario.titulo = data["titulo"]

    if "descricao" in data:
        formulario.descricao = data["descricao"]

    db.session.commit()

    return jsonify({
        "message": "Formulário atualizado com sucesso!"
    }), 200


# =========================================================
# DELETE FORMULÁRIO
# DELETE /formularios/<id>
# JWT
# =========================================================

@formularios_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_formulario(id):

    formulario = db.session.get(Formulario, id)

    if not formulario:
        return jsonify({
            "message": "Formulário não encontrado."
        }), 404

    db.session.delete(formulario)
    db.session.commit()

    return jsonify({
        "message": "Formulário excluído com sucesso!"
    }), 200