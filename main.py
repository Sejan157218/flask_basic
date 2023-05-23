from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from flask_restful import Resource, Api, marshal_with, fields


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/flask_test"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))


userSerializer = {
    "id" : fields.Integer,
    "name" : fields.String,
    "email" : fields.String
}
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

class addUser(Resource):
    # if request.method == 'POST':
    #     data = request.json
    #     users = User(id=data.get("id"), name=data.get("name"), email=data.get("email"))
    #     db.session.add(users)
    #     db.session.commit()
  
    #     return ""
    @marshal_with(userSerializer)
    def get(self):
        users = User.query.all()
        return users
    @marshal_with(userSerializer)
    def post(self):
        data = request.json
        users = User(id=data.get("id"), name=data.get("name"), email=data.get("email"))
        db.session.add(users)
        db.session.commit()
        return users
    
api.add_resource(addUser, '/users/')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')