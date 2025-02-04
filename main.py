import uuid
import time
from flask import Flask, session, request, redirect, render_template
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your actual secret key

# Define constants
DEVELOPER_URL = "http://127.0.0.1:5000/validate"
AUTHENTICATION_SERVICE_URL = "http://studentnet.cs.manchester.ac.uk/authenticate/"
AUTHENTICATION_LOGOUT_URL = "http://studentnet.cs.manchester.ac.uk/systemlogout.php"
users = {}


 

    
def get_authentication_url(command):
    csticket = session.get("csticket")
    url = f"{AUTHENTICATION_SERVICE_URL}?url={DEVELOPER_URL}&csticket={csticket}&version=3&command={command}"
    return url


  
def get_username():
    print(session)
    return request.args.get('username')


def is_ticket_in_request():
    csticket = request.args.get("csticket")
    return csticket and csticket.strip()

   
def is_csticket_matching_session():
    return request.args.get("csticket") == session.get("csticket")

@app.route('/')
def index():
    return render_template('index.html')

 
@app.route('/register')
def register():
    csticket = str(uuid.uuid4())
    session["csticket"] = csticket
    print('csticket: ', csticket)
    url = get_authentication_url("validate")
    print(url)
    return redirect(url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #add check of username and password
        if username in list(users.keys()):
            if password == users[username][0]:
                fullname = users[username][1]
                return show_page(username, fullname)
        return f'Incorrect credentials !'



@app.route('/validate')
def validate_new_user():
    username = get_username()
    fullname = request.args.get('fullname')
    print(username, fullname)
    if not is_csticket_matching_session():
        return f'Incorrect credentials !'
    if username not in list(users.keys()):
        return render_template('register.html', username = username, fullname = fullname)
    return render_template('index.html')


@app.route('/save_new_user/<username>', methods=['GET', 'POST'])
def save_new_user(username):
    if request.method == 'POST':
        password = request.form['password']
        fullname = request.form['fullname']
        users[username] = [password, fullname]
        return show_page(username, fullname)

@app.route('/user/<username>')
def show_page(username, fullname):
    print(users)
    return f'Hello {fullname} !'






if __name__ == '__main__':
    app.run(debug=True)
