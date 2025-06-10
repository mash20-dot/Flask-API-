from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
db = SQLAlchemy(app)
api = Api(app)

class Usermodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return f"User(name = {self.name}, email = {self.name})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")


user_args.add_argument('email', type=str, 
required=True, help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        Users = Usermodel.query.all()
        return Users
    
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = Usermodel(name=args["name"], email=args["emails"])
        db.session.add(user)
        db.session.commit()
        users = Usermodel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields) 
    def get(self, id):
        user = Usermodel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user


    @marshal_with(userFields) 
    def patch(self, id):
        args = user_args.parse_args()
        user = Usermodel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    @marshal_with(userFields) 
    def delete(self, id):
        user = Usermodel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = Usermodel.query.all()
        return users
    



api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>FLASK REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)