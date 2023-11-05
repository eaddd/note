from flask_restful import Resource, reqparse
from models.model import StoreModel
from schemas import schema
store_schema = schema.StoreSchema()
 
class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_name',type=str,required=True,help="Every store needs a name.")
 
    def get(self, id):
        store = StoreModel.query.filter_by(id=id).first_or_404()
        return store_schema.dump(store),200
 
    def post(self):
        data = self.parser.parse_args()
        store = store_schema.load(data)
 
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred"}, 500
 
        return store_schema.dump(store), 201
 
    
    def delete(self, id):
        StoreModel.query.filter_by(id=id).first_or_404()
        return {'message': 'Store deleted.'},200
    
    def put(self, id):
        data = self.parser.parse_args()
        store = StoreModel.query.filter_by(id=id).first_or_404()
 
        store.store_name = data['store_name']
        store.save_to_db()
 
        return store_schema.dump(store),200