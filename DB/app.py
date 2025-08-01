from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize the SQLAlchemy instance directly here
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:junaid1@localhost:5432/campus_corner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)

    from routes import todo_bp
    app.register_blueprint(todo_bp)
    
    # Create tables if they don’t exist
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return "Welcome to Campus Corner!"
    
    # Route to serve the HTML page
    @app.route('/tasks')
    def tasks_page():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
