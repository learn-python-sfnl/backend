from flask import Flask, jsonify, request, abort, Blueprint
from http import HTTPStatus
from uuid import uuid4

view = Blueprint('products', __name__)

products = [
        {
            'title': 'Книга по Python',
            'products': 'Книга',
            'id': uuid4().hex
        },

        {
            'title': 'Книга по JS',
            'products': 'Книга',
            'id': uuid4().hex
        }
]

storage = {product['id']: product for product in products}


@view.get('/')
def get_all_products():
    return jsonify(list(storage.values()))

@view.get('/<string:uid>')
def get_product_by_id(uid):
    product = storage.get(uid)
    if product:
        return jsonify(product), 200
    abort(404)

@view.post('/')
def add_product():
    product = request.json
    product['id'] = uuid4().hex
    storage[product['id']] = product
    return jsonify(product), 200

@view.put('/<string:uid>')
def update_product(uid):
    product = storage.get(uid)
    if uid not in storage:
        abort(404)

    payload = request.json
    product.update(payload)
    return jsonify(product), 200


@view.delete('/<string:uid>')
def delete_product(uid):
    if uid not in storage:
        abort(404)

    storage.pop(uid)
    return {}, 204
