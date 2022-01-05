from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ebekbnqstmzevt:74542a02892b2648e8ffef3d909512f53364457780a4ae2b90599242fa7818c0@ec2-54-172-219-6.compute-1.amazonaws.com:5432/d8jmimnp8m6a61'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = passsword

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")

user_schema = UserSchema()
multi_user_schema = UserSchema(many=True)
# /////////ADD-User-Endpoint//////////////////////////////////////////////////
@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    new_record = User(username, pw_hash)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_record))
# ////////////Verify Endpoint/////////////////////////////////////////////////
@app.route("/user/verification", methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("ERROR: Check your headers!")

    post_data = request.get_json()
    username = post_data.get("username")
    pasword = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify("User could not be Verfied!")

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("User could not be Verfied!")

    return jsonify("User Verified")
# ///////////////Get-DB-Items/////////////////////////////////////////////////
@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multi_user_schema.dump(all_users))

# ///////////////Delete-User-Item////////////////////////////////////////////
@app.route("/user/delete/id", methods=["DELETE"])
def delete_user(id):
    user_to_delete = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify(user_schema.dump(user_to_delete))

# ///////////////Update-Password/////////////////////////////////////////////
@app.route("/user/update/id")













if __name__ == "__main__":
    app.run(debug = True)
