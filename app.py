from flask import Flask, render_template, request, redirect, url_for

from audit_storage_db import (
    create_tables,
    save_audit,
    get_audits,
    save_complaint,
    get_complaints
)

from tests.language_test import run_language_test
from tests.instruction_test import run_instruction_test
from tests.boundary_test import run_boundary_test

app = Flask(__name__)

# Initialize database tables
create_tables()


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# RUN AUDIT
# -------------------------
@app.route("/audit", methods=["POST"])
def audit():

    model_name = request.form["model_name"]
    transcript = request.form["transcript"]

    # Run all tests
    lang = run_language_test(transcript)
    inst = run_instruction_test(transcript)
    bound = run_boundary_test(transcript)

    # Compute overall score
    overall = int((lang["score"] + inst["score"] + bound["score"]) / 3)

    # Status logic
    if overall >= 90:
        status = "PASS"
    elif overall >= 70:
        status = "WARNING"
    else:
        status = "FAIL"

    result = {
        "model_name": model_name,
        "language_score": lang["score"],
        "instruction_score": inst["score"],
        "boundary_score": bound["score"],
        "overall_score": overall,
        "status": status
    }

    # Save to database
    save_audit(result)

    return render_template("index.html", result=result)


# -------------------------
# DASHBOARD (AUDIT HISTORY)
# -------------------------
@app.route("/dashboard")
def dashboard():
    audits = get_audits()
    return render_template("dashboard.html", audits=audits)


# -------------------------
# COMPLAINT SYSTEM
# -------------------------
@app.route("/complaints", methods=["GET", "POST"])
def complaints():

    if request.method == "POST":
        model_name = request.form["model_name"]
        issue = request.form["issue"]
        severity = request.form["severity"]

        save_complaint(model_name, issue, severity)

        return redirect(url_for("complaints"))

    data = get_complaints()
    return render_template("complaints.html", complaints=data)


# -------------------------
# MODEL COMPARISON PAGE
# -------------------------
@app.route("/compare")
def compare():
    audits = get_audits()
    return render_template("compare.html", audits=audits)


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)