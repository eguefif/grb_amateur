import httpx

BACKEND_URL = "http://127.0.0.1:8000/"


def get_users():
    request = httpx.get(f"{BACKEND_URL}users/")
    return request.json()


def post_event(event):
    response = httpx.post(f"{BACKEND_URL}events/", json=event)
    print(response)
