import httpx

BACKEND_URL = "http://127.0.0.1:8000/"


def get_users():
    request = httpx.get(f"{BACKEND_URL}users/")
    print(request.json())
    return request.json()


def post_event(event):
    if 'position' in event['notice_type'].lower():
        print(event)
        response = httpx.post(f"{BACKEND_URL}events/position", json=event)
    elif 'alert' in event['notice_type'].lower():
        response = httpx.post(f"{BACKEND_URL}events/", json=event)
    else:
        print("Unknown type of message")
    print(response)
