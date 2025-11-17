import datetime
import os
from dotenv import load_dotenv
from gcn_kafka import Consumer
from confluent_kafka import TopicPartition

load_dotenv()

client_id = os.getenv("GCN_CLIENT")
key = os.getenv("GCN_KEY")
consumer = Consumer(client_id=client_id, client_secret=key)

topics = [
        "gcn.classic.text.FERMI_GBM_ALERT",
        "gcn.classic.text.FERMI_GBM_FIN_POS",
        "gcn.classic.text.FERMI_GBM_GND_POS",
        "gcn.classic.text.FERMI_GBM_POS_TEST",
    ]

# get messages occurring 3 days ago
timestamp1 = int((datetime.datetime.now() - datetime.timedelta(days=3)).timestamp() * 1000)
timestamp2 = timestamp1 + 86400000 # +1 day

start = consumer.offsets_for_times(
    [TopicPartition(topics[0], 0, timestamp1),
    TopicPartition(topics[1], 0, timestamp1),
    TopicPartition(topics[2], 0, timestamp1),
     ])
end = consumer.offsets_for_times(
    [TopicPartition(topics[0], 0, timestamp2),
    TopicPartition(topics[1], 0, timestamp2),
    TopicPartition(topics[2], 0, timestamp2),
     ])

consumer.assign(start)
print("\n\n",  "*" * 20, "GND_ALERT")
for message in consumer.consume(end[0].offset - start[0].offset, timeout=1):
    print(f"topic={message.topic()}, offset={message.offset()}")
    print(message.value())
    print()

print("\n\n",  "*" * 20, "GND_FIN_POS")
for message in consumer.consume(end[1].offset - start[1].offset, timeout=1):
    print(message.value())

print("\n\n",  "*" * 20, "GND_GND_POS")
for message in consumer.consume(end[2].offset - start[2].offset, timeout=1):
    print(message.value())
