import os
from kafka import KafkaConsumer, TopicPartition
from json import loads
from util.K8Util import K8Util

hostname = os.getenv('COMPUTERNAME')
node_port_id = K8Util.get_node_port_number()

consumer = KafkaConsumer(bootstrap_servers=[f'{hostname}:{node_port_id}'],
                         group_id='my-group2',
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

tp = TopicPartition(topic='gen-basic1', partition=0)
consumer.assign([tp])
consumer.seek(tp, 0)

for message in consumer:
    msg = message.value
    print(f'Message {msg}')
