from flask import Blueprint, request, session, redirect, url_for, render_template
from models import db, User
import uuid

auth = Blueprint('auth', __name__)

AUTHENTICATION_SERVICE_URL = "http://studentnet.cs.manchester.ac.uk/authenticate/"
DEVELOPER_URL = "http://127.0.0.1:5000/auth/validate"


def get_authentication_url(command):
    csticket = session.get("csticket")
    return f"{AUTHENTICATION_SERVICE_URL}?url={DEVELOPER_URL}&csticket={csticket}&version=3&command={command}"


def is_csticket_matching_session():
    return request.args.get("csticket") == session.get("csticket")


@auth.route('/register')
def register():
    csticket = str(uuid.uuid4())
    session["csticket"] = csticket
    return redirect(get_authentication_url("validate"))


@auth.route('/validate')
def validate_new_user():
    username = request.args.get('username')
    fullname = request.args.get('fullname')

    if not is_csticket_matching_session():
        return "Incorrect credentials!"

    user = User.query.filter_by(username=username).first()

    if not user:
        return render_template('register.html', username=username, fullname=fullname)

    return redirect(url_for('auth.login'))


@auth.route('/save_new_user/<username>', methods=['POST'])
def save_new_user(username):
    password = request.form['password']
    fullname = request.form['fullname']
    
    name_parts = fullname.strip().split(" ",1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    new_user = User(
        username=username,
        password=password,
        first_name=first_name,
        last_name= last_name)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.user_id
            return redirect(url_for('routes.todo_page'))

        return "Incorrect credentials!"

    return render_template('index.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect("http://studentnet.cs.manchester.ac.uk/systemlogout.php")
