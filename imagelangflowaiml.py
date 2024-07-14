import requests
import json

url = "https://api.aimlapi.com/chat/completions"

payload = json.dumps({
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://i.postimg.cc/D0pgqf31/burger.webp"
          }
        }
      ]
    }
  ]
})

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer 0f6cfe3d82254c6f83395b4a6bdc32fd'
}

response = requests.post(url, headers=headers, data=payload)
message = response.json()["choices"][0]["message"]["content"]
print(message)
