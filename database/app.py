from flask import Flask, render_template
from config import Config
from models import db
from routes import routes
from auth import auth 

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

#Blueprints
app.register_blueprint(routes)
app.register_blueprint(auth, url_prefix='/auth')  # authentication routes use /auth

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
