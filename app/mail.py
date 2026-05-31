import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_report_email(report):
    """Envia e-mail com os dados da ocorrência. Silencioso em caso de falha."""
    try:
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        recipients = current_app.config.get("MAIL_RECIPIENTS", [])

        if not username or not password:
            return False

        subject = f"[Ilumina VP] Nova Ocorrencia #{report.id} - {report.category_label}"

        body = (
            "Prezado(a),\n\n"
            "Uma nova ocorrencia de iluminacao publica foi registrada pela comunidade "
            "no sistema Ilumina VP.\n\n"
            "DADOS DA OCORRENCIA\n"
            "--------------------\n"
            f"ID: #{report.id}\n"
            f"Tipo: {report.category_label}\n"
            f"Descricao: {report.description}\n"
            f"Localizacao: Lat {report.latitude}, Lng {report.longitude}\n"
            f"Google Maps: https://www.google.com/maps?q={report.latitude},{report.longitude}\n"
            f"Data do registro: {report.created_at.strftime('%d/%m/%Y %H:%M')}\n"
            f"Reportado por: {report.reporter_name}\n"
            f"E-mail do cidadao: {report.reporter_email or 'Nao informado'}\n\n"
            "--------------------\n\n"
            "Solicitamos providencias para resolucao do problema relatado.\n\n"
            "Atenciosamente,\n"
            "Sistema Ilumina VP\n"
            "Vicente Pires, DF\n"
        )

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, recipients, msg.as_string())

        return True

    except Exception:
        return False
