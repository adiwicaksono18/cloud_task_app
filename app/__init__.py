import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    default_database_url = "sqlite:///cloudtask.db"
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-key"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", default_database_url),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
