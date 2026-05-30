import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_report_email(report):
    """Envia e-mail com os dados da ocorrência para os destinatários configurados."""
    username = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]
    recipients = current_app.config["MAIL_RECIPIENTS"]

    if not username or not password:
        current_app.logger.warning("SMTP não configurado. E-mail não enviado.")
        return False

    subject = f"[Ilumina VP] Nova Ocorrência #{report.id} — {report.category_label}"

    body = f"""Prezado(a),

Uma nova ocorrência de iluminação pública foi registrada pela comunidade no sistema Ilumina VP.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DADOS DA OCORRÊNCIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• ID: #{report.id}
• Tipo: {report.category_label}
• Descrição: {report.description}
• Localização: Lat {report.latitude}, Lng {report.longitude}
• Google Maps: https://www.google.com/maps?q={report.latitude},{report.longitude}
• Data do registro: {report.created_at.strftime('%d/%m/%Y às %H:%M')}
• Reportado por: {report.reporter_name}
• E-mail do cidadão: {report.reporter_email or 'Não informado'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Solicitamos providências para resolução do problema relatado.

Atenciosamente,
Sistema Ilumina VP
Vicente Pires, DF
"""

    try:
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, recipients, msg.as_string())

        current_app.logger.info(f"E-mail enviado para {recipients} — Ocorrência #{report.id}")
        return True

    except Exception as e:
        current_app.logger.error(f"Erro ao enviar e-mail: {e}")
        return False
