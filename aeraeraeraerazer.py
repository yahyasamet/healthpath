import requests
import requests
import json

# Your API key
api_key = '17fb61bf44e84f4085b988909705e2df'



prompt = "hello"


# Define the URL and headers
url = 'https://api.aimlapi.com/chat/completions'
headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 17fb61bf44e84f4085b988909705e2df"
}

# Define the data payload
data = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "you are a diabetics doctor you will help the patient based on their question you are a master at meal prep AI assistant for diabetics."},
        {"role": "user", "content": prompt}
    ]
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Parse the response JSON
data = response.json()
content = data['choices'][0]['message']['content']
print(content)

