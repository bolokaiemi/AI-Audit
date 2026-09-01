# FAQ

## General
- **What is AI Auditor V0.1?**
  AI Auditor V0.1 is a web‑based platform that evaluates AI systems for risks such as bias, fairness, privacy, security, and ethical impact. It provides automated checks and detailed reports.

- **Who should use AI Auditor?**
  Developers, data scientists, product managers, and compliance teams who want to assess AI model behaviour before deployment.

## Usage
- **How do I start an audit?**
  Go to **Start Audit**, fill in the prompt/model/system or upload a test case, select the categories to evaluate, and click **Run Audit**.

- **Where can I find previous audit results?**
  Open **Audit History** from the dashboard and click any entry to view its results.

- **Can I export a report?**
  Yes – on the **Audit Results** page click **Export** and choose PDF or JSON.

## Categories
- **What does the "Fairness" category check?**
  It looks for disparate impact across protected attributes and ensures equitable treatment.
- **What is covered under "Privacy"?**
  Detection of personally identifiable information (PII) leakage in model outputs.

## Troubleshooting
- **Why is my audit taking a long time?**
  Large inputs or many selected categories increase runtime. Try narrowing the scope or using a smaller test case.
- **I received an error "Model not found".**
  Verify the model identifier is correct and that the model is accessible from the server.
- **The assistant does not answer my question.**
  Make sure the query relates to documented platform features; otherwise the assistant will inform you that the information is unavailable.

Feel free to add more questions as the platform evolves.
