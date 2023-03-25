import logging

from flask import Flask, jsonify

from backend.db import db_session
from backend.errors import AppError
from backend.views import categories, products

logger = logging.getLogger(__name__)

app = Flask(__name__)
APP_PORT = 8000


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    return jsonify(error=str(error)), error.status


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('hello world')
    app.register_blueprint(categories.view, url_prefix='/api/v1/categories')
    app.register_blueprint(products.view, url_prefix='/api/v1/products')

    app.teardown_appcontext(shutdown_session)

    app.run(port=APP_PORT)


def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    main()
