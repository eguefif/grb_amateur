from dotenv import load_dotenv
import os

from message_client import GCNClient
from backend_calls import post_event


def notify_users(message):
    print("-" * 50)
    print("New message from GCN: ", message["title"], "\n")
    post_event(message)
    print()


def get_message_client():
    if os.getenv("TEST_CLIENT") == "True":
        return GCNClient(test=True)
    return GCNClient(test=False)


def main():
    if os.getenv("PROD") == "True":
        load_dotenv("/run/secrets/alertsys-secret")
    message_client = get_message_client()
    print("Starting monitoring alert")

    while True:
        try:
            for message in message_client.consume(timeout=1):
                if "test position" not in message["notice_type"]:
                    notify_users(message)
        except Exception as e:
            print("Fatal error: ", e)


if __name__ == "__main__":
    main()
