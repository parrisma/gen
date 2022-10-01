from time import sleep
from json import dumps
from kafka import KafkaProducer


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


producer = KafkaProducer(bootstrap_servers=['arther-2:31211'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'number': e}
    future = record_metadata = producer.send('gen-basic', value=data)
    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
        # Successful result returns assigned partition and offset
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)
    except Exception as exp:
        print(f'{exp}')
        pass
    producer.flush()
