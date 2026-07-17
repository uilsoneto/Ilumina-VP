from flask import Blueprint, render_template, jsonify, redirect, url_for

from app.models import Report

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/mapa")
def mapa():
    return redirect(url_for("main.index"))


@main_bp.route("/api/reports")
def api_reports():
    reports = Report.query.all()
    data = [
        {
            "id": r.id,
            "lat": r.latitude,
            "lng": r.longitude,
            "description": r.description,
            "category": r.category_label,
            "status": r.status_label,
            "reporter": r.reporter_name,
            "photo": r.photo_url,
            "created_at": r.created_at.strftime("%d/%m/%Y %H:%M"),
        }
        for r in reports
    ]
    return jsonify(data)


@main_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")
