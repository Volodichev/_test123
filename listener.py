import json
from time import sleep
import requests

from core.settings import MESSAGE_CONFIRM_URL, FORBIDDEN_WORDS, KAFKA_TOPIC, KAFKA_SERVERS, TOKEN_JWT_URL, DEFAULT_USER, \
    BASE_URL
from services.kafka_services import get_from_kafka, get_consumer
from services.text_services import text_contains_any_word


class SomeError(Exception):
    pass


headers = {'Content-Type': 'application/json'}
result = requests.post(url=TOKEN_JWT_URL, data=DEFAULT_USER, headers=headers)
print(f'{result=}')
# Token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2ODgzMzkwLCJqdGkiOiJmNjg4ZmViODNlMDg0NjUwODE0ZWI4ODU1ZWFmYTk0ZCIsInVzZXJfaWQiOjJ9.bZwrh-w3yxKUrXDLb1mPTw2RYsn1pDrXjco6pXs1GUk"

while True:
    consumer = get_consumer(topic_name=KAFKA_TOPIC,
                            # group_id='my-group',
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            bootstrap_servers=KAFKA_SERVERS)

    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))

        data = json.loads(message.value.decode('utf-8'))
        print(f'message {data=}')
        message_id = data.get("message_id")
        message_text = data.get("text")
        try:
            if message_text and message_id:
                success_result = not text_contains_any_word(text=message_text, words=FORBIDDEN_WORDS)
                print(f'message {success_result=}')

                params = {
                    "message_id": message_id,
                    "success": success_result
                }

                headers = {'Authorization': f'Bearer {Token}'}
                result = requests.post(url=MESSAGE_CONFIRM_URL, data=params, headers=headers)
                print(f'{result=}')
            else:
                raise SomeError
        except:
            print(SomeError)
        sleep(1)

    sleep(1)

    # break
