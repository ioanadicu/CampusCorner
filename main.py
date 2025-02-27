import uuid
import time
from flask import Flask, session, request, redirect, render_template, url_for


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
    print('redirect to UoM login')
    return redirect(url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print('Got username and password: ', username, password)
    if len(username)>0:
        print('Got username and password: ', username, password)
            #add check of username and password
        if username in list(users.keys()):
            if password == users[username][0]:
                print('correct creds!')
                fullname = users[username][1]
                return redirect(url_for('show_page', username = username, fullname = fullname))
        return f'Incorrect credentials !'



@app.route('/validate')
def validate_new_user():
    username = get_username()
    fullname = request.args.get('fullname')
    print('Got username and fullname from UoM', username, fullname)
    if not is_csticket_matching_session():
        return f'Incorrect credentials !'
    if username not in list(users.keys()):
        print('This is a new usr, so create a password')
        return render_template('register.html', username = username, fullname = fullname)
    return render_template('index.html')


@app.route('/save_new_user/<username>', methods=['GET', 'POST'])
def save_new_user(username):
    if request.method == 'POST':
        password = request.form['password']
        fullname = request.form['fullname']
        users[username] = [password, fullname]
        print('Saving new user with creds', username, password)
        return redirect(url_for('show_page', username = username, fullname = fullname))

@app.route('/user/<username>', methods=['GET'])
def show_page(username):
    fullname = request.args.get('fullname')
    print('This is a page for user', fullname)
    return render_template('user.html', fullname = fullname, username=username)

@app.route('/user/<username>/monitor')
def show_monitor(username):
    return render_template('monitor.html')






if __name__ == '__main__':
    app.run(debug=True)
