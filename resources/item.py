from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

"""
"stores" is the name of the blueprint. This will be shown in the documentation and is prepended to the endpoint names when you use url_for (we won't use it).
__name__ is the "import name".
The description will be shown in the documentation UI.
"""
blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    #get a single item 
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    #delete a single item
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privelege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    #update an item
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
        # item exists, we can put it's values ok
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
        # item does not exist, we now creare a new one with the data we got
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemsList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    #get all the items
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    #create an item
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")
        return item