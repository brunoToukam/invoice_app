from flask import Flask
from app.models import db

DATABASE_URI = "sqlite:///factures.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)
    return app


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database Initialized!")


if __name__ == "__main__":
    init_db()
