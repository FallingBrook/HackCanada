import requests

API_KEY = "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"  # Replace with your API key
url = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "sonar-pro",  # Choose a model (e.g., pplx-70b-chat)
    "messages": [
        {"role": "user", "content": "What is PyCharm?"}
    ]
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    answer = response.json()["choices"][0]["message"]["content"]
    print(answer)
else:
    print(f"Error: {response.status_code}", response.text)