#导入必要的包
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
 
class config():
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "data.db"))

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app) #创建db
api = Api(app)
#先导入Item和Store类
from resources.item import Item
from resources.store import Store

api.add_resource(Item,'/item/<int:id>')
api.add_resource(Item,'/item',endpoint='create_item',methods=['POST'])
api.add_resource(Store,'/store/<int:id>')
api.add_resource(Store,'/store',endpoint='create_store',methods=['POST'])
 
 
if __name__ == "__main__":
    db = SQLAlchemy(app)
    db.drop_all()
    db.create_all()
    app.run(debug=True)