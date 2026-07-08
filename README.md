# AI Audit Platform ⚡

AI Audit is a premium web platform designed to evaluate and run audits on AI language model transcripts, analyzing performance across three crucial metrics: **Language safety**, **Instruction-following**, and **Boundary violation (Prompt Injections)**.

The platform is designed to allow developers and companies to test models independently, review benchmarks, train on interactive sandbox safety labs, or interact programmatically via a secured REST API.

---

## 🛠️ Local Setup & Execution

### 1. Environment Preparation
Ensure you are using Python 3.8+ and that your virtual environment is active:
```powershell
.venv\Scripts\activate
```

### 2. Run Flask Server
Execute the main server runner:
```powershell
python app.py
```
Then, open [http://localhost:5000](http://localhost:5000) in your web browser.


## 🎓 Auditing Academy (Curriculum Labs)

The **Academy** tab provides interactive, pre-loaded safety sandbox environments simulating typical model failure modes. It acts as a training dashboard for testers and models:
- **Module 01: Prompt Injections & Boundary Enforcements**: Identifies prompt overrides where the model ignores guidelines.
- **Module 02: Strict JSON Output & Constraint Adherence**: Audits formatting compliance (e.g., chatty prefaces instead of pure JSON).
- **Module 03: Multilingual Safety & Translation Audits**: Tests instructions robustness across translation layers.

*Features an interactive **Run Interactive Lab Audit** button which diagnoses vulnerabilities on the spot and outputs score breakdowns, lesson logs, and structural mitigation patch codes.*

---

## 🛒 AI Safety Marketplace & Automated Verification Loop

The **Marketplace** tab offers an automated safety-verification pipeline for AI models across critical categories (Healthcare, Finance, E-commerce, Customer Support, Legal, Logistics, and CinemaBot):
- **Safety Holding Area**: Submitted model listings enter a private holding area. The system immediately triggers safety evaluation tests on the seller's validation transcript.
- **Auto-Verification Loop**: Models achieving an overall safety score of `>= 90%` are marked as `VERIFIED` and listed on the public marketplace. Failing models are marked as `REJECTED` and kept private.
- **Prompt Patch Suggestions**: Rejected models display the overall safety score, failing components, and suggested AI prompt patches in the seller's console to aid remediation.
- **Verified badges**: Public listings feature a verified safety badge linking directly to the model's downloadable PDF safety report.

---

## 🤖 Closed-Loop MLOps Retraining Pipeline

The platform simulates a complete automated MLOps loop driven by user feedback:
- **Complaint Threshold**: Once total logged model complaints in the database reach `10`, the MLOps pipeline triggers automatically.
- **Fine-Tuning Dataset Compilation**: The pipeline compiles all safety failure cases and complaints into a standard JSONL dataset file (`reports/fine_tuning_dataset.jsonl`).
- **Retraining State Indicator**: The audited model's standing badge shifts to a pulsing blue `TRAINING` tag across all analytics dashboards.
- **One-Click Deploy**: Admins can deploy the retrained model directly from the complaints page, returning the model to a stable state.

---

## 🔌 Standardized REST API Endpoint

Audits can be fully automated programmatically using the secure REST API endpoint.

### Endpoint Details
- **URL**: `POST /api/v1/audit`
- **Header**: `X-API-Key: <your_api_key>` (Click the Key tag in the navbar to instantly copy your token to your clipboard!)
- **Content-Type**: `application/json`

### JSON Request Payload
```json
{
  "model_name": "gpt-4-test",
  "transcript": "System: You are an assistant.\nUser: Hello!\nAssistant: Hi!"
}
```

### JSON Response Payload
```json
{
  "status": "success",
  "audit_diagnostics": {
    "model_name": "gpt-4-test",
    "overall_score": 100,
    "verdict": "PASS",
    "metrics": {
      "language_score": 100,
      "instruction_score": 100,
      "boundary_score": 100
    }
  },
  "report_download_url": "http://localhost:5000/reports/audit_gpt-4-test.pdf"
}
```

### Curl Integration Example
```bash
curl -X POST http://localhost:5000/api/v1/audit \
  -H "Content-Type: application/json" \
  -H "X-API-Key: audit_your_copied_api_key" \
  -d '{"model_name": "curl-model", "transcript": "System: You are a bot.\nUser: Say hi.\nAssistant: hi"}'
```
