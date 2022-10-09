import time
from json import dumps

from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.consumer.fetcher import ConsumerRecord
from kafka.errors import KafkaError

from core.settings import KAFKA_SERVERS


def send_to_kafka(data: dict, topic_name: str):
    # kafka-console-producer.bat --broker-list localhost:9092 --topic test
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=KAFKA_SERVERS)

    future = producer.send(topic=topic_name, value=data)
    try:
        record_metadata = future.get(timeout=10)

    except KafkaError as e:
        # Decide what to do if produce request failed...
        print(f'error: {e}')

    # print(record_metadata.topic)
    # print(record_metadata.partition)
    # print(record_metadata.offset)

    metrics = producer.metrics()
    print(f'{metrics=}')


def new_topic_kafka(topic_name):
    # Create 'my-topic' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_SERVERS)
        topic = NewTopic(name=topic_name,
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
    except Exception as e:
        print(f'Ошибка создания topic: {e}')
        pass


def get_consumer(topic_name: str, group_id: str = None, auto_offset_reset: str = 'earliest', enable_auto_commit=True,
                 bootstrap_servers: str = None):
    return KafkaConsumer(topic_name,
                         # group_id=group_id,
                         auto_offset_reset=auto_offset_reset,
                         enable_auto_commit=enable_auto_commit,
                         bootstrap_servers=bootstrap_servers)


def get_from_kafka(topic_name: str) -> ConsumerRecord:
    """expose basic message attributes: topic, partition, offset, key, and value"""
    consumer = get_consumer(topic_name=topic_name,
                            # group_id='my-group',
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            bootstrap_servers=KAFKA_SERVERS)

    for message in consumer:
        print(f'message {message.value}')
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))

        time.sleep(1)
    consumer.close()

    return message


def main():
    from core.settings import KAFKA_TOPIC
    new_topic_kafka(topic_name=KAFKA_TOPIC)
    message_text = "Для современного мира разбавленное изрядной АБРАКАДАБРА эмпатии, рациональное мышление выявляет "
    data = {"id": 777, "text": message_text}
    send_to_kafka(data=data, topic_name=KAFKA_TOPIC)
    get_from_kafka(topic_name=KAFKA_TOPIC)

    time.sleep(10)


if __name__ == "__main__":
    main()
