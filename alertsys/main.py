from dotenv import load_dotenv
from message_client import MessageClient


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
            print(value)


if __name__ == "__main__":
    main()
