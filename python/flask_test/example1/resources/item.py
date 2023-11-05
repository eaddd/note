from flask_restful import Resource, reqparse
from models.model import ItemModel, StoreModel
from schemas import schema
item_schema = schema.ItemSchema()
 
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help="Every item needs a name.")
 
    def get(self, id):
        item = ItemModel.query.filter_by(id=id).first_or_404()
        return item_schema.dump(item)
 
    def post(self):
        data = self.parser.parse_args()
        if not StoreModel.query.filter_by(id=data['storeid']).first():
            return {'message':'商店不存在'},400
 
        item = item_schema.load(data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
 
        return item_schema.dump(item),201
 
    def delete(self, id):
        item = ItemModel.fquery.filter_by(id=id).first_or_404()
        item.delete_from_db()
        return {'message': 'Item deleted.'},200
 
    def put(self, id):
        data = Item.parser.parse_args()
        item = ItemModel.query.filter_by(id=id).first_or_404()
 
        for column in item.__table__.columns:
            if column.name != 'id': setattr(item,column.name,data.get(column.name))
 
        item.save_to_db()
        return item_schema.dump(item)