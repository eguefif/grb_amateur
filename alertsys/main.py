from dotenv import load_dotenv
from message_client import MessageClient
import httpx

import json

def get_users():
    request = httpx.get("http://127.0.0.1:8000/users/")
    return request.json()

def notify_users(message):
    users = get_users()
    print("-" * 50)
    print("New message from GCN: ", message, "\n")
    for user in users:
        print(" " * 5, f"Notifying user {user["email"]}")
    print()

def main():
    load_dotenv()
    message_client = MessageClient(test=True)

    while True:
        for message in message_client.consume(timeout=1):
            if message.error():
                print("Error: ", message.error())
                continue
            print(f"topic={message.topic()}, offset={message.offset()}")
            value = message.value()
            notify_users(value)


if __name__ == "__main__":
    main()
