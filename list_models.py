import urllib.request
import json

key = "AQ.Ab8RN6J0k9B7UjQmruO9s2hb2CZYXvkORhHkcIeP__HsJQDj6A"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print("AVAILABLE MODELS:")
        for m in data.get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print("-", m.get("name"))
except Exception as e:
    print("ERROR:", e)
