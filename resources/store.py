import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema 

"""
"stores" is the name of the blueprint. This will be shown in the documentation and is prepended to the endpoint names when you use url_for (we won't use it).
__name__ is the "import name".
The description will be shown in the documentation UI.
"""
blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    #get a single store
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


    #delete single store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store is deleted."}

@blp.route("/store")
class StoreList(MethodView):
    #get all the stores data 
   
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    #create a store
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists."
            )
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the store.")
        return store