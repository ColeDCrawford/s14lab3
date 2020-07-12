from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.user import db, User
from modules.userform import UserForm
import names
import random

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usersdb'
from flask_heroku import Heroku
app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    # Query all
    users = User.query.all()

    if 'success' in globals():
        return render_template("index.html.j2", users=users, success=success)
    elif request.args.get('success') is not None:
        success = request.args.get('success')
        return render_template("index.html.j2", users=users, success=success)
    else:
        return render_template("index.html.j2", users=users)

@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    if request.method == 'GET':
        if request.args.get('first_name') is not None and request.args.get('age') is not None:
            first_name = request.args.get('first_name')
            age = request.args.get('age')
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index', success="User added!"))
        else:
            return render_template("adduser.html.j2", form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index', success="User added!"))
        else:
            return render_template('adduser.html', form=form, error="User not added")

@app.route('/user/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if request.method == 'GET':
        if 'success' in globals():
            return render_template("user.html.j2", success=success, user=user)
        elif request.args.get('success') is not None:
            success = request.args.get('success')
            return render_template("user.html.j2", success=success, user=user)
        else:
            return render_template("user.html.j2", user=user)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        users = User.query.all()
        data = {
            "success": f"User {user_id} deleted"
        }
        return jsonify(data)
    if request.method == 'PUT':
        data = request.get_json()
        user.first_name = data.get('first_name');
        user.age = data.get('age');
        db.session.commit()
        user = User.query.filter_by(user_id=user_id).first()
        data = {
            "success": f"User {user_id} updated"
        }
        return jsonify(data)

@app.route('/updateuser/<int:user_id>', methods=['GET'])
def updateUser(user_id):
    form = UserForm()
    user = User.query.filter_by(user_id=user_id).first()
    if request.method == 'GET':
        return render_template("updateuser.html.j2", user=user, form=form)

@app.route('/mock', methods=['GET'])
def mockData():
    new = 3 #default
    input = int(request.args.get('new'))
    if isinstance(input, int):
        new = input

    def createMockUser():
        first_name = names.get_first_name()
        age = random.randrange(0,100,1)
        new_user = User(first_name=first_name, age=age)
        db.session.add(new_user)
        db.session.commit()

    for i in range(0, new):
        createMockUser()

    users = User.query.all()
    return render_template("index.html.j2", users=users, success=f"{new} new mock users created")
