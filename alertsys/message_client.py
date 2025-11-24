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
        if not self.test:
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
        exit()

    def _parse_message(self, message) -> dict:
        print("New Message")
        print(message)
        message = message.decode()
        # In position message, GRB_RA and GRB_DEC are multiline fields
        # We remove the return line to parse them easily
        message = message.strip()

        splits = message.split("\n")

        data = {}
        splits = iter(splits)
        while True:
            try:
                entry = next(splits)
            except StopIteration:
                break
            if len(entry) >= 1:
                key, value = entry.split(":", 1)
                key = key.strip().lower()
                if key == "2nd_most_likely":
                    key = "second_most_likely"
                value = value.strip()
                if key in data.keys() and key == "comments":
                    current_value = data[key]
                    if isinstance(current_value, str):
                        data[key] = current_value + " | " + value
                    else:
                        data[key] = [value]
                elif key in ["grb_ra", "grb_dec"]:
                    data[key] = self._get_coord(value, splits)
                else:
                    data[key] = value
        return data

    def _get_coord(self, line1, splits):
        line2 = next(splits)
        line3 = next(splits)
        return self._format_grb_position(".".join([line1, line2, line3]))

    def _format_grb_position(self, data):
        """grb_ra and grb_dec has a lot of empty space that needs to be trim"""
        return ", ".join([position.strip() for position in data.split(",")])
