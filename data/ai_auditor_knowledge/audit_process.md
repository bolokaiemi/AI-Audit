# Audit Process

This guide walks users through the complete lifecycle of an AI audit in **AI Auditor V0.1**.

## 1. Start an Audit
1. Navigate to **Start Audit** from the dashboard.
2. Enter the **Prompt** you want to evaluate, or provide a **Model**, **System description**, or a **Test case**.
3. Select the relevant **Audit Categories** (e.g., Fairness, Bias, Privacy, Security, Explainability).
4. Click **Run Audit**.

## 2. Audit Execution
- The backend sends the request to the audit engine.
- The engine analyses the input using a suite of checks for each selected category.
- Progress is shown in real‑time on the page.

## 3. Review Results
1. Once the audit completes, you are redirected to the **Audit Results** page.
2. Examine the **Risk Summary** which highlights high‑risk findings.
3. Dive into each category for detailed explanations, examples, and recommended remediation steps.

## 4. Save & Share
- Click **Save** to store the audit in **Audit History**.
- Use the **Export** button to download a PDF or JSON report.
- Share the report link with collaborators via the **Share** feature.

## 5. Iterate
- Based on the findings, adjust your model, prompt, or system description.
- Re‑run the audit to see if the risk score improves.

### Tips
- Start with a broad set of categories, then narrow down to the most relevant ones.
- Use the **School Project** examples as templates for common audit scenarios.
