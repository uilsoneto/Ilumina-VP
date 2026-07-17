import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///ilumina_vp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload de fotos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # SMTP Gmail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Destinatários das ocorrências
    MAIL_RECIPIENTS = [
        "ouvidoria@vicentepires.df.gov.br",
        "ouvidoria.bsb@neoenergia.com",
    ]
