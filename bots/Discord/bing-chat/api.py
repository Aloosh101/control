import requests

url = "https://www.bing.com/chat"
payload = {"message": "هلا؟"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(data)