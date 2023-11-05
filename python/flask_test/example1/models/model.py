from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
 
class ItemModel(db.Model):
 
    __tablename__ = 't_item'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Integer)
    storeid = db.Column(db.Integer,db.ForeignKey('t_store.id')) #外建关联
    
    def __init__(self,name,price,storeid):
        self.name = name
        self.price = price
        self.storeid = storeid
 
    def save_to_db(self):  #添加到数据库中 -- 后面resource类会使用到
        db.session.add(self)
        db.session.commit()
 
    def delete_from_db(self): #从数据库中删除该记录
        db.session.delete(self)
        db.session.commit()

class StoreModel(db.Model):
 
    __tablename__ = 't_store'
 
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column('store_name',db.String(80), unique=True)
    items = db.relationship('ItemModel',backref='store')
    
    def __init__(self,store_name):
        self.store_name = store_name
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
 
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
 
    def __repr__(self):
        return self.store_name