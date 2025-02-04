import uuid
import time
from flask import Flask, session, request, redirect, render_template_string
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your actual secret key

# Define constants
DEVELOPER_URL = "http://127.0.0.1:5000"
AUTHENTICATION_SERVICE_URL = "http://studentnet.cs.manchester.ac.uk/authenticate/"
AUTHENTICATION_LOGOUT_URL = "http://studentnet.cs.manchester.ac.uk/systemlogout.php"
users = []


 

    
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
    try:
        username = get_username()
        print('username', username)
        if username==None:
            
            csticket = str(uuid.uuid4())
            session["csticket"] = csticket
            print('csticket: ', csticket)
            url = get_authentication_url("validate")
            print(url)
            return redirect(url)
        # Display authenticated user details
        print('authenticated')
        if not username in users:
            users.append(username) 
        fullname = request.args.get('fullname')
        
        return show_page(username, fullname)
    except Exception as e:
        return str(e)

 

@app.route('/user/<username>')
def show_page(username, fullname):
    return f'Hello {fullname} !'






if __name__ == '__main__':
    app.run(debug=True)
