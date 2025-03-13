import requests

def send_message(recipient_id, message):
    """
    يرسل رسالة إلى Facebook.

    Args:
        recipient_id: معرف المستلم.
        message: الرسالة.
    """
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"

    url = "https://graph.facebook.com/v12.0/me/messages"
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
    }
    response = requests.post(url, json=data, headers={"Authorization": f"Bearer {api_key}"})
    return response

def main():
    recipient_id = "1234567890"
    message = "مرحبًا!"

    

    response = send_message(recipient_id, message)

    if response.status_code == 200:
        print("تم إرسال الرسالة بنجاح!")
    else:
        print("حدث خطأ:", response.status_code)

if __name__ == "__main__":
    main()
