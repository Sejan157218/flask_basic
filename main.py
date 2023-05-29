from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request, jsonify
from flask_restful import Resource, Api, marshal_with, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, os, json
from Auth_decoretor.decoretor import token_required


app = Flask(__name__)
api = Api(app)

SECRET_KEY = "django-insecure-0=26u4h(j%g6(s%etg6tg%+fllvj0vx@sam*q)17zb$nk_b7(9"
app.config['SECRET_KEY'] = SECRET_KEY


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/flask_test"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    def as_dict(self):
        obj_d = {
        "id" : self.id,
        "name" : self.name,
        "email" : self.email,
        }
        return obj_d

userSerializer = {
    "id" : fields.Integer,
    "name" : fields.String,
    "email" : fields.String,
    "password" : fields.String
}
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def encrypt_password(self, password):
    """Encrypt password"""
    return generate_password_hash(password)


class addUser(Resource):
    @marshal_with(userSerializer)
    def get(self):
        users = User.query.all()
        return users
    # @marshal_with(userSerializer)
    def post(self):
        data = request.json
        users = User(id=data.get("id"), name=data.get("name"), email=data.get("email"), password=encrypt_password(self,data.get("password")))
        db.session.add(users)
        db.session.commit()
        token = jwt.encode(
                    {"user_id": users.id},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
            )
        return jsonify(token = token, user=users.as_dict())
api.add_resource(addUser, '/users/')


class userLogin(Resource):

    def post(self):
        data = request.json
        user =  User.query.filter_by(id=data.get("id")).first()
        if not user or not check_password_hash(user.password, data.get("password")):
    
            return {"error" :"error"}
        token = jwt.encode(
                    {"user_id": user.id},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
            )
        return jsonify(token = token, user=user.as_dict())
api.add_resource(userLogin, '/login/')

class allUser(Resource):
    @token_required
    @marshal_with(userSerializer)
    def get(self, *args, **kwargs):
        print("djbfhvsdhvzh", args,kwargs)
        users = User.query.all()
        return users
    @token_required
    @marshal_with(userSerializer)
    def post(self, *args, **kwargs):
        data = request.json
        print("djbfhvsdhvzh", data)
        users = User.query.all()
        return users
api.add_resource(allUser, '/all-user/')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')