import os
import time
from gcn_kafka import Consumer

class MessageClient:
    def __init__(self, test=False):
        self.test = test
        if self.test == False:
            client_id = os.getenv("GCN_CLIENT")
            key = os.getenv("GCN_KEY")
            self.consumer = Consumer(client_id=client_id, client_secret=key)

            self.consumer.subscribe(
                [
                    "gcn.classic.text.FERMI_GBM_ALERT",
                    "gcn.classic.text.FERMI_GBM_FIN_POS",
                    "gcn.classic.text.FERMI_GBM_GND_POS",
                    "gcn.classic.text.FERMI_GBM_POS_TEST",
                ]
            )

    def consume(self, timeout=1):
        if self.test:
            print("test")
            yield from self.run_test()
        else:
            for message in self.consumer.consume(timeout=timeout):
                message
                yield

    def run_test(self):
        yield Message()
        time.sleep(1)


class Message:
    def __init__(self):
        ...

    def error(self):
        return False

    def topic(self):
        return "GCR"

    def offset(self):
        return "None"

    def value(self):
        return "Hello, World"

