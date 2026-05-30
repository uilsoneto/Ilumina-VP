from datetime import datetime, timezone

from app import db


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="poste_apagado")
    status = db.Column(db.String(30), nullable=False, default="pendente")
    reporter_name = db.Column(db.String(150), nullable=False, default="Anônimo")
    reporter_email = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    CATEGORIES = [
        ("poste_apagado", "Poste Apagado"),
        ("area_escura", "Área Escura"),
        ("iluminacao_fraca", "Iluminação Fraca"),
        ("poste_danificado", "Poste Danificado"),
    ]

    STATUSES = [
        ("pendente", "Pendente"),
        ("em_analise", "Em Análise"),
        ("resolvido", "Resolvido"),
    ]

    @property
    def category_label(self):
        return dict(self.CATEGORIES).get(self.category, self.category)

    @property
    def status_label(self):
        return dict(self.STATUSES).get(self.status, self.status)
