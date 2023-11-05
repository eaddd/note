from flask import Flask,jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api,request
import os


app=Flask(__name__)

class config():
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "example.db"))

app.config.from_object(config)
api=Api(app)
db=SQLAlchemy(app)
ma=Marshmallow(app)
class test(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(24))
    age=db.Column(db.Integer)
    money=db.relationship('moneys',uselist=False)  #

class moneys(db.Model):
    id = db.Column(db.Integer,db.ForeignKey('test.id'))
    money = db.Column(db.String(),primary_key=True)



class UserSchema(ma.ModelSchema):
    class Meta:
        model = test

class MoneySchema(ma.ModelSchema):
    class Meta:
        model = moneys

@app.route('/')
def index():
    one_user = test.query.all()
    user_schema = UserSchema(many=True) #用已继承ma.ModelSchema类的自定制类生成序列化类
    print(one_user)
    output = user_schema.dumps(one_user) #生成可序列化对象
    return output


@app.route("/test", methods=["POST"])
def add_user():
    user_schema = UserSchema(many=False)
    ss=user_schema.load(request.get_json(force=True))
    print (ss)
    db.session.add(ss)
    db.session.commit()
    return user_schema.dump(test.query.filter(test.id==request.json['id']).first())


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)

