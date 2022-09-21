from flask import Flask, request, jsonify, session, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)



#----------Start ToDo db ----------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(144), nullable=False)


    def __init__(self, content):
        self.content = content

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content')

todo_schema = TodoSchema()
multiple_todo_schema = TodoSchema(many=True)



#----------start Todo Endpoints ----------
@app.route('/todo/add', methods=['POST'])
def add_todo():
    post_data = request.get_json()
    content = post_data.get('content')

    new_todo = Todo(content)

    db.session.add(new_todo)
    db.session.commit()

    return jsonify('Todo added successfully')

@app.route('/todo/get', methods=["GET"])
def get_todos():
    todo = db.session.query(Todo).all()
    return jsonify(multiple_todo_schema.dump(todo))

@app.route('/todo/get/<user_fk>', methods=['GET'])
def get_todo(user_fk):
    todo = db.session.query(Todo).filter(Todo.user_fk == User.id).all()
    return jsonify(multiple_todo_schema.dump(todo))

@app.route('/todo/delete/<id>', methods = ["DELETE"])
def delete_todo(id):
    todo = db.session.query(Todo).filter(Todo.id == id).first()
    db.session.delete(todo)
    db.session.commit()

    return jsonify('Goodbye Todo')





if __name__ == "__main__":
    app.run(debug=True)
