import os
from json import dumps
from kafka import KafkaProducer
from util.K8Util import K8Util

hostname = os.getenv('COMPUTERNAME')
node_port_id = K8Util.get_node_port_number()

producer = KafkaProducer(bootstrap_servers=[f'{hostname}:{node_port_id}'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'number': e}
    future = producer.send('gen-basic1', value=data)
    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
    except Exception as exp:
        print(f'{exp}')
        pass
    producer.flush()
