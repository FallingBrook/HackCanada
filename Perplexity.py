import requests

API_KEY = "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"  # Replace with your API key
url = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}



def GetPerplexityResponse(question, parameter):
    data = {
        "model": "sonar-pro",  # Choose a model (e.g., pplx-70b-chat)
        "messages": [
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "return_related_questions": False
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    else:
        print(f"Error: {response.status_code}", response.text)
        return None

GetPerplexityResponse("3 names for dogs", "HI")