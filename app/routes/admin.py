from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from functools import wraps

from app import db
from app.models import Report

admin_bp = Blueprint("admin", __name__)

# Senha simples para acesso admin (sem necessidade de banco de usuários)
ADMIN_PASSWORD = "iluminavp2024"


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Acesso administrativo concedido.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Senha incorreta.", "danger")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Você saiu do painel administrativo.", "info")
    return redirect(url_for("main.index"))


@admin_bp.route("/")
@admin_required
def dashboard():
    total = Report.query.count()
    pendentes = Report.query.filter_by(status="pendente").count()
    em_analise = Report.query.filter_by(status="em_analise").count()
    resolvidos = Report.query.filter_by(status="resolvido").count()

    recent_reports = Report.query.order_by(Report.created_at.desc()).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        total=total,
        pendentes=pendentes,
        em_analise=em_analise,
        resolvidos=resolvidos,
        reports=recent_reports,
    )


@admin_bp.route("/ocorrencias")
@admin_required
def ocorrencias():
    page = request.args.get("page", 1, type=int)
    status_filter = request.args.get("status", "")

    query = Report.query.order_by(Report.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.paginate(page=page, per_page=15, error_out=False)

    return render_template(
        "admin/ocorrencias.html",
        reports=pagination.items,
        pagination=pagination,
        statuses=Report.STATUSES,
        current_status=status_filter,
    )


@admin_bp.route("/ocorrencia/<int:report_id>/status", methods=["POST"])
@admin_required
def atualizar_status(report_id):
    report = Report.query.get_or_404(report_id)
    new_status = request.form.get("status")

    valid_statuses = [s[0] for s in Report.STATUSES]
    if new_status in valid_statuses:
        report.status = new_status
        db.session.commit()
        flash(f"Ocorrência #{report.id} atualizada para '{dict(Report.STATUSES)[new_status]}'.", "success")

    return redirect(request.referrer or url_for("admin.ocorrencias"))


@admin_bp.route("/ocorrencia/<int:report_id>/enviar-email", methods=["POST"])
@admin_required
def enviar_email(report_id):
    report = Report.query.get_or_404(report_id)
    destinatario = request.form.get("destinatario", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    if not destinatario:
        flash("Informe o e-mail do destinatário.", "danger")
        return redirect(url_for("admin.ocorrencias"))

    # Monta o corpo do e-mail (simulação — em produção usar SMTP)
    corpo_email = f"""
Assunto: Ocorrência de Iluminação Pública - Vicente Pires #{report.id}

Prezado(a),

Segue relato de ocorrência registrada pela comunidade no sistema Ilumina VP:

- ID: #{report.id}
- Tipo: {report.category_label}
- Descrição: {report.description}
- Local: Lat {report.latitude}, Lng {report.longitude}
- Data do registro: {report.created_at.strftime('%d/%m/%Y às %H:%M')}
- Reportado por: {report.reporter_name}

{mensagem}

Solicitamos providências para resolução do problema.

Atenciosamente,
Sistema Ilumina VP — Vicente Pires, DF
"""

    # Em produção, aqui entraria o envio real via SMTP
    # Por ora, registramos que o e-mail foi "enviado"
    flash(
        f"E-mail preparado para {destinatario} referente à ocorrência #{report.id}. "
        f"(Em produção, seria enviado via SMTP)",
        "success",
    )

    # Atualiza status para "em_analise" se ainda estiver pendente
    if report.status == "pendente":
        report.status = "em_analise"
        db.session.commit()

    return redirect(url_for("admin.ocorrencias"))


@admin_bp.route("/exportar")
@admin_required
def exportar():
    """Exporta todas as ocorrências em formato CSV."""
    import csv
    from io import StringIO
    from flask import Response

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Categoria", "Descrição", "Latitude", "Longitude", "Status", "Reportado por", "Data"])

    reports = Report.query.order_by(Report.created_at.desc()).all()
    for r in reports:
        writer.writerow([
            r.id,
            r.category_label,
            r.description,
            r.latitude,
            r.longitude,
            r.status_label,
            r.reporter_name,
            r.created_at.strftime("%d/%m/%Y %H:%M"),
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=ocorrencias_ilumina_vp.csv"
    return response
