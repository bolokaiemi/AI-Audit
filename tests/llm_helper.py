import os
import json
import urllib.request
import urllib.error

def query_openai(system_prompt: str, user_prompt: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip() or api_key == "YOUR_OPENAI_API_KEY_HERE":
        return None
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            content = res_json["choices"][0]["message"]["content"]
            return json.loads(content)
    except Exception as e:
        print(f"[LLM Evaluator Error] OpenAI API request failed: {e}")
        return None
