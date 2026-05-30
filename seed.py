"""Script para popular o banco com dados de exemplo."""

from app import create_app, db
from app.models import Report

app = create_app()

with app.app_context():
    db.create_all()

    if Report.query.count() == 0:
        reports_data = [
            {
                "latitude": -15.8012,
                "longitude": -48.0198,
                "description": "Poste completamente apagado na esquina da Rua 4 com Rua 8. Local muito escuro à noite.",
                "category": "poste_apagado",
                "reporter_name": "Maria Silva",
                "reporter_email": "maria.silva@email.com",
            },
            {
                "latitude": -15.7985,
                "longitude": -48.0215,
                "description": "Trecho de aproximadamente 100m sem nenhuma iluminação. Pedestres precisam usar lanterna do celular.",
                "category": "area_escura",
                "reporter_name": "João Santos",
                "reporter_email": None,
            },
            {
                "latitude": -15.8035,
                "longitude": -48.0180,
                "description": "Poste com lâmpada piscando intermitentemente. Iluminação muito fraca.",
                "category": "iluminacao_fraca",
                "reporter_name": "Ana Oliveira",
                "reporter_email": "ana.oliveira@email.com",
            },
            {
                "latitude": -15.7998,
                "longitude": -48.0230,
                "description": "Poste inclinado após colisão de veículo. Fiação exposta e sem iluminação.",
                "category": "poste_danificado",
                "reporter_name": "Carlos Souza",
                "reporter_email": None,
            },
            {
                "latitude": -15.8050,
                "longitude": -48.0165,
                "description": "Dois postes apagados consecutivos próximo à praça. Área de risco à noite.",
                "category": "poste_apagado",
                "status": "em_analise",
                "reporter_name": "Anônimo",
                "reporter_email": None,
            },
        ]

        for data in reports_data:
            report = Report(**data)
            db.session.add(report)

        db.session.commit()
        print("✅ Banco populado com dados de exemplo!")
    else:
        print("ℹ️  Banco já contém dados.")
