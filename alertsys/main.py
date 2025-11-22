from dotenv import load_dotenv
import sys
import os
from smtp_client import SMTPClient

from message_client import GCNClient
from backend_calls import get_users, post_event


import json


def notify_users(message):
    #users = get_users()
    print("-" * 50)
    print("New message from GCN: ", message["title"], "\n")
    post_event(message)
    #smtp_client = SMTPClient()
    #user_emails = [user["email"] for user in users]
    #smtp_client.send_emails(user_emails, message)
    print()


def get_message_client():
    if os.getenv("TEST_CLIENT") == "True":
        return GCNClient(test=True)
    return GCNClient(test=False)


def main():
    load_dotenv()
    message_client = get_message_client()
    print("Starting monitoring alert")

    while True:
        for message in message_client.consume(timeout=1):
            notify_users(message)


if __name__ == "__main__":
    main()
