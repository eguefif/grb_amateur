import httpx

BACKEND_URL = "http://127.0.0.1:8000/"


def get_users():
    request = httpx.get(f"{BACKEND_URL}users/")
    return request.json()


def post_event(event):
    if event['notice_type'].lower().contains('position'):
        response = httpx.post(f"{BACKEND_URLS}events/position/", json=event)
    elif event['notice_type'].lower().contains('alert'):
        response = httpx.post(f"{BACKEND_URL}events/", json=event)
    else:
        print("Unknown type of message")
    print(response)
