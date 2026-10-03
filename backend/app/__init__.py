import os

from dotenv import load_dotenv
from flask import Flask, app

from .extensions import cors, db, migrate

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "sqlite:///app.db",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": os.getenv(
                    "FRONTEND_ORIGIN",
                    "http://localhost:5173",
                )
            }
        },
    )
    
    from . import models  # noqa: F401

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app