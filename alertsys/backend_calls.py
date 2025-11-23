import httpx
import time
import hmac
import os
import hashlib


BACKEND_URL = "http://127.0.0.1:8000/"


def get_signature(timestamp, event):
    SECRET = os.getenv("SECRET_KEY")

    trigger_num = event["trigger_num"]
    message = f"{timestamp}:{trigger_num}".encode()
    signature = hmac.new(SECRET.encode(), message, hashlib.sha256).hexdigest()
    return signature


def post_event(event):
    timestamp = str(time.time())
    headers = {"X-Signature": get_signature(timestamp, event), "X-Timestamp": timestamp}

    if "position" in event["notice_type"].lower():
        print(event)
        response = httpx.post(
            f"{BACKEND_URL}events/position", json=event, headers=headers
        )
    elif "alert" in event["notice_type"].lower():
        response = httpx.post(f"{BACKEND_URL}events/", json=event, headers=headers)
    else:
        print("Unknown type of message")
    print(response)
