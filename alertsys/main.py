from dotenv import load_dotenv
import sys
import os

from message_client import MessageClient
from backend_calls import get_users, post_event


import json
def notify_users(message):
    users = get_users()
    print("-" * 50)
    print("New message from GCN: ", message['title'], "\n")
    post_event(message)
    for user in users:
        print(" " * 5, f"Notifying user {user["email"]}")
    print()

def get_message_client():
    if os.getenv("TEST_CLIENT") == 'True':
        return MessageClient(test=True)
    MessageClient()

def main():
    load_dotenv()
    message_client = get_message_client()

    while True:
        for message in message_client.consume(timeout=1):
            notify_users(message)


if __name__ == "__main__":
    main()
