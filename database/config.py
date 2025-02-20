import os
from dotenv import load_dotenv

load_dotenv()
# env variables


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://campus_user:junaid1@localhost/CampusCorner")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    