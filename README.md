# AI Auditor Platform ⚡

AI Auditor is a premium web platform designed to evaluate and run audits on AI language model transcripts, analyzing performance across three crucial metrics: **Language**, **Instruction-following**, and **Boundary violation**.

---

## 🗝️ Testing Credentials

To facilitate testing the web application locally or online, use the following pre-provisioned credentials:

### 1. Platform Administrator (Admin Role)
- **Username**: `admin`
- **Password**: `admin123`
- **Permissions**: Full access to the **Complaints & Admin** center, where you can submit model issues and download all audit reports compiled into a single ZIP file.

### 2. Standard Tester (User Role)
- **Username**: `tester`
- **Password**: `tester123`
- **Permissions**: Access to the core features including running transcript audits, viewing the analytics **Dashboard**, and inspecting **Model Benchmark Comparison** leaderboards.

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
