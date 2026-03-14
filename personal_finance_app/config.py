import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "finance.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER') or 'aryanmali450@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') or 'your-app-password'
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER') or 'aryanmali450@gmail.com'