import os
import time
from gcn_kafka import Consumer

# This import is used by the test mode
from dummy_message import fake_messages

## There are several types of message from GCN
# * GBM_Alert
# * GBM_FIN_POS
# * GBM_GRD_POS


class GCNClient:
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
                if message.error():
                    print("Error: ", message.error())
                    continue
                print(f"Alert received: {message.offset()}")
                yield self._parse_message(message.value())

    def run_test(self):
        for message in fake_messages:
            if len(message) >= 1:
                message = self._parse_message(message)
                yield message
            time.sleep(1)

    def _parse_message(self, message):
        print("New Message")
        print(message)
        message = message.decode()
        # In position message, GRB_RA and GRB_DEC are multiline fields
        # We remove the return line to parse them easily
        message.replace(",\n", ", ")
        splits = message.split("\n")

        data = {}
        for entry in splits:
            print("First line: ", entry)
            if len(entry) >= 1:
                key, value = entry.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                if key in data.keys():
                    current_value = data[key]
                    if isinstance(current_value, str):
                        data[key] = current_value + " | " + value
                    else:
                        data[key] = [value]
                else:
                    data[key] = value
        if "grb_ra" in data.keys():
            data["grb_ra"] = self._format_grb_position(data["grb_ra"])
        return data

    def _format_grb_position(self, data):
        """grb_ra and grb_dec has a lot of empty space that needs to be trim"""
        splits = data[","]
        return ", ".join([position.strip() for position in data.split(",")])
