import logging

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotfoundError
from backend.models import Product

logger = logging.getLogger(__name__)


class PgStorage:

    def add(self, title: str, category_id: int, user_id: int) -> Product:
        add_product = Product(
            title=title,
            category_id=category_id,
            user_id=user_id,
        )
        db_session.add(add_product)
        try:
            db_session.commit()
        except IntegrityError:
            logger.exception('Can not add product')
            raise ConflictError(entity='products', method='add')
        return add_product

    def get_all(self) -> list[Product]:
        return Product.query.all()

    def get_by_id(self, uid: int) -> Product:
        product = Product.query.get(uid)
        if not product:
            raise NotfoundError(entity='products', method='get_by_id')
        return product

    def get_for_user(self, uid: int) -> list[Product]:
        return Product.query.filter(Product.user_id == uid).all()

    def update(self, uid: int, title: str, category_id: int) -> Product:
        product = Product.query.get(uid)
        if not product:
            raise NotfoundError(entity='products', method='update')
        product.title = title
        product.category_id = category_id
        try:
            db_session.commit()
        except IntegrityError:
            logger.exception('Can not update product')
            raise ConflictError(entity='products', method='update')
        return product

    def delete(self, uid: int):
        product = Product.query.get(uid)
        if not product:
            raise NotfoundError(entity='products', method='delete')
        db_session.delete(product)
        try:
            db_session.commit()
        except IntegrityError:
            logger.exception('Can not delete product')
            raise ConflictError(entity='products', method='delete')
