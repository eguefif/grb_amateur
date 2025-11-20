import os
import time
from gcn_kafka import Consumer

# This import is used by the test mode
from message_client import fake_messages

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
            yield from self.run_test()
        else:
            for message in self.consumer.consume(timeout=timeout):
                Message(message.value)
                yield

    def run_test(self):
        for message in fake_messages:
            if len(message) >= 1 and :
                yield Message(message)
            time.sleep(1)


class Message:

    def __init__(self, message):
        self.message = message
        self.data = self._parse_message(message.decode())

    def get_key(key):
        if key in self.data.keys:
            self.data[key]
        else:
            None

    def _parse_message(self, message):
        splits = message.split('\n')

        data = {}
        for entry in splits:
            if len(entry) >= 1:
                key, value = entry.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key in h.keys():
                    current_value = h[key]
                    if isinstance(former_value, list):
                        current_value.append(value)
                        data[key] = current_value
                    else:
                        data[key] = [value]
                else:
                    data[key] = value
        return data
