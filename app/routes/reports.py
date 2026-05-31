from flask import Blueprint, render_template, redirect, url_for, flash, request

from app import db
from app.models import Report
from app.mail import send_report_email

reports_bp = Blueprint("reports", __name__)


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

        report = Report(
            latitude=lat,
            longitude=lng,
            description=description,
            category=category,
            reporter_name=reporter_name,
            reporter_email=reporter_email,
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
