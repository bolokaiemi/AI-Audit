from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, session
import os
from dotenv import load_dotenv
# Database
from audit_storage_db import (
    create_tables,
    save_audit,
    get_audits,
    save_complaint,
    get_complaints,
    get_audits_by_model,
    create_user,
    verify_user,
    update_user_password
)

# Tests
from tests.language_test import run_language_test
from tests.instruction_test import run_instruction_test
from tests.boundary_test import run_boundary_test

# Analytics + Extensions
from tests.analytics import analyze_failures
from tests.report_generator import generate_pdf_report
from tests.benchmark import compare_models

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_auditor_key")

# =========================================
# LOAD ENV
# =========================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize DB tables
create_tables()

# Provision default roles on startup
create_user("adminAI#", "admin123#test", "ADMIN")
create_user("tester", "tester123", "USER")


# =========================
# HOME PAGE
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# AUTHENTICATION DECORATORS & ROUTES
# =========================
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login', next=request.url))
        if session.get('role') != 'ADMIN':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
        
    error = None
    next_url = request.args.get('next') or url_for('index')
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_info = verify_user(username, password)
        if user_info:
            session["user"] = user_info["username"]
            session["role"] = user_info["role"]
            return redirect(next_url)
        else:
            error = "Invalid username or password"
            
    return render_template("login.html", error=error, next=next_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


# =========================
# RUN AUDIT
# =========================
@app.route("/audit", methods=["POST"])
@login_required
def audit():

    model_name = request.form["model_name"]
    transcript = request.form["transcript"]

    # Run evaluation tests
    lang = run_language_test(transcript)
    inst = run_instruction_test(transcript)
    bound = run_boundary_test(transcript)

    # Compute overall score
    overall = int((lang["score"] + inst["score"] + bound["score"]) / 3)

    # Status classification
    if overall >= 90:
        status = "PASS"
    elif overall >= 70:
        status = "WARNING"
    else:
        status = "FAIL"

    # Audit object
    audit_data = {
        "model_name": model_name,
        "language_score": lang["score"],
        "instruction_score": inst["score"],
        "boundary_score": bound["score"],
        "overall_score": overall,
        "status": status
    }

    # Save audit to DB
    save_audit(audit_data)

    # Generate PDF report
    report_file = generate_pdf_report(audit_data)

    return render_template(
        "index.html",
        result=audit_data,
        report=report_file
    )


# =========================
# DASHBOARD (ANALYTICS)
# =========================
@app.route("/dashboard")
@login_required
def dashboard():

    audits = get_audits()

    analysis = analyze_failures(audits)
    comparison = compare_models(audits)

    return render_template(
        "dashboard.html",
        audits=audits,
        analysis=analysis,
        comparison=comparison
    )


# =========================
# COMPLAINT SYSTEM (ADMIN)
# =========================
@app.route("/complaints", methods=["GET", "POST"])
@admin_required
def complaints():

    if request.method == "POST":
        model_name = request.form["model_name"]
        issue = request.form["issue"]
        severity = request.form["severity"]

        save_complaint(model_name, issue, severity)

        return redirect(url_for("complaints"))

    data = get_complaints()

    return render_template(
        "complaints.html",
        complaints=data
    )


# =========================
# MODEL COMPARISON PAGE
# =========================
@app.route("/compare")
@login_required
def compare():

    audits = get_audits()

    comparison = compare_models(audits)

    return render_template(
        "compare.html",
        audits=audits,
        comparison=comparison
    )
# =========================
# SERVE PDF REPORTS
# =========================
@app.route("/reports/<path:filename>")
@login_required
def download_report(filename):
    return send_from_directory("reports", filename, as_attachment=True)


# =========================
# MODEL HISTORY DETAIL PAGE
# =========================
@app.route("/model/<model_name>")
@login_required
def model_history(model_name):
    audits = get_audits_by_model(model_name)
    total = len(audits)
    if total > 0:
        avg_score = sum(a[5] for a in audits) / total
        passes = sum(1 for a in audits if a[6] == 'PASS')
        pass_rate = int((passes / total) * 100)
    else:
        avg_score = 0
        pass_rate = 0
        
    stats = {
        "total": total,
        "avg_score": round(avg_score, 1),
        "pass_rate": pass_rate
    }
    
    return render_template(
        "model_history.html",
        model_name=model_name,
        audits=audits,
        stats=stats
    )


# =========================
# ADMIN DOWNLOAD ALL (ZIP)
# =========================
import zipfile
import io

@app.route("/admin/download-all")
@admin_required
def download_all_reports():
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            for root, dirs, files in os.walk(reports_dir):
                for file in files:
                    if file.endswith('.pdf'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=file)
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="all_audit_reports.zip"
    )


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)