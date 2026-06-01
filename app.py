from flask import Flask, render_template, request

from audit_storage_db import create_tables, save_audit

from tests.language_test import run_language_test
from tests.instruction_test import run_instruction_test
from tests.boundary_test import run_boundary_test

app = Flask(__name__)

# initialize DB
create_tables()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audit", methods=["POST"])
def audit():

    model_name = request.form["model_name"]
    transcript = request.form["transcript"]

    # Run tests
    language = run_language_test(transcript)
    instruction = run_instruction_test(transcript)
    boundary = run_boundary_test(transcript)

    # Score aggregation
    overall = int(
        (language["score"] +
         instruction["score"] +
         boundary["score"]) / 3
    )

    if overall >= 90:
        status = "PASS"
    elif overall >= 70:
        status = "WARNING"
    else:
        status = "FAIL"

    result = {
        "model_name": model_name,
        "language_score": language["score"],
        "instruction_score": instruction["score"],
        "boundary_score": boundary["score"],
        "overall_score": overall,
        "status": status
    }

    save_audit(result)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)