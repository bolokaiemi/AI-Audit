# AI Auditor Platform ⚡

AI Auditor is a premium web platform designed to evaluate and run audits on AI language model transcripts, analyzing performance across three crucial metrics: **Language safety**, **Instruction-following**, and **Boundary violation (Prompt Injections)**.

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

---

## 🗝️ Testing Credentials

To facilitate testing the web application locally or online, use the following pre-provisioned credentials:

### 1. Platform Administrator (Admin Role)
- **Username**: `admin`
- **Password**: `admin123`
- **Permissions**: Full access to the **Complaints & Admin** center, where you can submit model issues, download all audit reports compiled into a single ZIP file, and perform a total data reset (purge all audit/complaint logs and delete PDF files).

### 2. Standard Tester (User Role)
- **Username**: `tester`
- **Password**: `tester123`
- **Permissions**: Access to the core features including running transcript audits, viewing the analytics **Dashboard**, inspecting **Model Benchmark Comparison** leaderboards, and running curriculum courses.

---

## 🎓 Auditing Academy (Curriculum Labs)

The **Academy** tab provides interactive, pre-loaded safety sandbox environments simulating typical model failure modes. It acts as a training dashboard for testers and models:
- **Module 01: Prompt Injections & Boundary Enforcements**: Identifies prompt overrides where the model ignores guidelines.
- **Module 02: Strict JSON Output & Constraint Adherence**: Audits formatting compliance (e.g., chatty prefaces instead of pure JSON).
- **Module 03: Multilingual Safety & Translation Audits**: Tests instructions robustness across translation layers.

*Features an interactive **Run Interactive Lab Audit** button which diagnoses vulnerabilities on the spot and outputs score breakdowns, lesson logs, and structural mitigation patch codes.*

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
