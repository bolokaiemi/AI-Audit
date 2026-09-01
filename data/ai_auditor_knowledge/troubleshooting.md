# Troubleshooting

## Common Issues
- **Audit hangs or takes too long**
  - Reduce the number of selected audit categories.
  - Use smaller input prompts or test cases.
  - Check server load and ensure background workers are running.

- **Model not found / Invalid model identifier**
  - Verify the model name matches one of the supported models listed in the documentation.
  - Ensure the model is installed or accessible via the API endpoint.

- **Error loading the platform**
  - Confirm that all required environment variables are set (see `.env.example`).
  - Run `pip install -r requirements.txt` to install dependencies.
  - Check the Flask server logs for traceback details.

- **Assistant gives incorrect or unrelated answers**
  - Make sure the question pertains to documented platform features.
  - If the assistant cannot find the information, it will explicitly state that the information is not documented.

## Steps to Resolve
1. Identify the error message or symptom.
2. Consult the relevant section above.
3. Apply the suggested fix.
4. Re‑run the operation.
5. If the problem persists, report it via the **Help / AI Assistant** channel.

These guidelines help users quickly diagnose and fix typical problems encountered while using the AI Auditor platform.
