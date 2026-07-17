import os
import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename

from app import db
from app.models import Report
from app.mail import send_report_email

reports_bp = Blueprint("reports", __name__)


def allowed_file(filename):
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "webp"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def save_photo(file):
    """Salva foto e retorna o nome do arquivo."""
    if not file or file.filename == "":
        return None
    if not allowed_file(file.filename):
        return None

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filename


@reports_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "poste_apagado")
        reporter_name = request.form.get("reporter_name", "").strip() or "Anônimo"
        reporter_email = request.form.get("reporter_email", "").strip() or None

        if not latitude or not longitude:
            flash("Selecione um ponto no mapa.", "danger")
            return render_template("reports/novo.html", categories=Report.CATEGORIES)

        if not description:
            flash("Descreva o problema encontrado.", "danger")
            return render_template("reports/novo.html", categories=Report.CATEGORIES)

        try:
            lat = float(latitude)
            lng = float(longitude)
        except (ValueError, TypeError):
            flash("Coordenadas inválidas.", "danger")
            return render_template("reports/novo.html", categories=Report.CATEGORIES)

        # Salva foto se enviada
        photo_filename = None
        if "photo" in request.files:
            photo_filename = save_photo(request.files["photo"])

        report = Report(
            latitude=lat,
            longitude=lng,
            description=description,
            category=category,
            reporter_name=reporter_name,
            reporter_email=reporter_email,
            photo_filename=photo_filename,
            status="em_analise",
        )
        db.session.add(report)
        db.session.commit()

        # Envia e-mail para ouvidoria (silencioso se SMTP não configurado)
        send_report_email(report)

        flash("Ocorrência registrada com sucesso! Obrigado por contribuir.", "success")
        return redirect(url_for("main.index"))

    return render_template("reports/novo.html", categories=Report.CATEGORIES)


@reports_bp.route("/lista")
def lista():
    page = request.args.get("page", 1, type=int)
    status_filter = request.args.get("status", "")

    query = Report.query.order_by(Report.created_at.desc())

    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.paginate(page=page, per_page=10, error_out=False)

    return render_template(
        "reports/lista.html",
        reports=pagination.items,
        pagination=pagination,
        statuses=Report.STATUSES,
        current_status=status_filter,
    )


@reports_bp.route("/<int:report_id>")
def detalhe(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template("reports/detalhe.html", report=report)
