from flask import Blueprint, request, session, redirect, url_for, render_template
from models import db, User
import uuid

auth = Blueprint('auth', __name__)

AUTHENTICATION_SERVICE_URL = "http://studentnet.cs.manchester.ac.uk/authenticate/"
DEVELOPER_URL = "http://127.0.0.1:5000/auth/validate"


def get_authentication_url(command):
    csticket = session["csticket"]
    return f"{AUTHENTICATION_SERVICE_URL}?url={DEVELOPER_URL}&csticket={csticket}&version=3&command={command}"


def is_csticket_matching_session():
    print('csticket from uom', request.args.get("csticket"))
    print(session["csticket"])
    print('go to uom')
    return True


@auth.route('/register')
def register():
    csticket = str(uuid.uuid4())
    session["csticket"] = csticket
    print('generated csticket', csticket)
    print('register')
    return redirect(get_authentication_url("validate"))


@auth.route('/validate')
def validate_new_user():
    username = request.args.get('username')
    fullname = request.args.get('fullname')

    user = User.query.filter_by(username=username).first()
    if user:
        return "You already have an account. Go to login"
    if not is_csticket_matching_session():
        return "Ticket is not matching"
    if not user:
        return render_template('register.html', username=username, fullname=fullname)

    return redirect(url_for('auth.login'))


@auth.route('/save_new_user/<username>', methods=['POST'])
def save_new_user(username):
    password = request.form['password']
    fullname = request.form['fullname']
    

    new_user = User(
        username=username,
        password=password,
        fullname=fullname)

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
            print("Logged in user_id:", user.user_id)  # Debug print

            fullname = user.fullname
            return redirect(url_for('auth.show_page', username= username, fullname= fullname))

        return "Incorrect credentials!"

    return render_template('index.html')

@auth.route('/user/<username>', methods=['GET'])
def show_page(username):
    fullname = request.args.get('fullname')
    print('This is a page for user', fullname)
    return render_template('user.html', fullname = fullname, username=username)

@auth.route('/user/<username>/monitor')
def show_monitor(username):
    return render_template('monitor.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect("http://studentnet.cs.manchester.ac.uk/systemlogout.php")
