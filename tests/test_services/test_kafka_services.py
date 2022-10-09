from services.kafka_services import send_to_kafka, get_from_kafka, new_topic_kafka
from core.settings import KAFKA_TOPIC


def test_send_to_kafka():
    message_text = "Для современного мира разбавленное изрядной АБРАКАДАБРА эмпатии, рациональное мышление выявляет "
    data = {"id": 777, "text": message_text}
    send_to_kafka(data=data, topic_name=KAFKA_TOPIC)


def test_get_from_kafka():
    get_from_kafka(topic_name=KAFKA_TOPIC)


def test_topics():
    new_topic_kafka(topic_name=KAFKA_TOPIC)
    message_text = "Для современного мира разбавленное изрядной АБРАКАДАБРА эмпатии, рациональное мышление выявляет "
    data = {"id": 777, "text": message_text}
    send_to_kafka(data=data, topic_name=KAFKA_TOPIC)
    get_from_kafka(topic_name=KAFKA_TOPIC)
