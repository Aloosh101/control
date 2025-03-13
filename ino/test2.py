
import requests


account_sid = "your_account_sid"
auth_token = "your_auth_token"


sender = "whatsapp:+your_number"
receiver = "whatsapp:+specific_number"


message = "Hello, this is a test message from Bing."


url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


payload = {
    "From": sender,
    "To": receiver,
    "Body": message
}


headers = {
    "Authorization": f"Basic {account_sid}:{auth_token}"
}


response = requests.post(url, data=payload, headers=headers)


print(response.status_code)
print(response.text)
