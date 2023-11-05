from models import model
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields,post_load
 
class ItemSchema(ModelSchema):
 
    id = fields.Integer(dump_only=True) #read_only字段
    name = fields.Str()
    price = fields.Float()
    storeid = fields.Integer(load_only=True) #write_only字段
    store = fields.Str()
    
    #反序列化
    @post_load
    def make_item(self, data, **kwargs):
        return model.ItemModel(**data)
 
    class Meta:
        model = model.ItemModel

class StoreSchema(ModelSchema):
    id = fields.Integer(dump_only=True)
    store_name = fields.Str()
    #返回items的列表
    items = fields.Nested(ItemSchema,many=True,dump_only=True,only=('id','name','price'))
 
    @post_load
    def create_store(self, data, **kwargs):
        return model.StoreModel(**data)
    
    class Meta:
        model = model.StoreModel