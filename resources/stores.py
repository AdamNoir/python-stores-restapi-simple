import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema, UpdateStoreSchema


blp = Blueprint("stores", __name__, "Operations on stores")


@blp.route("/store/<store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store was deleted."}

    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store:
            store.name = store_data["name"]
        else:
            abort(404, message="store not found")
        return store


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Name already exists.")
        except SQLAlchemyError:
            abort(500, message="Error ocurred while insert store.")
