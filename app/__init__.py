import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def migrate_db():
    """Adiciona colunas novas ao banco existente se necessário."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    columns = [col["name"] for col in inspector.get_columns("reports")]

    with db.engine.connect() as conn:
        if "photo_filename" not in columns:
            conn.execute(text("ALTER TABLE reports ADD COLUMN photo_filename VARCHAR(255)"))
            conn.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.reports import reports_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        try:
            migrate_db()
        except Exception:
            pass
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    return app
