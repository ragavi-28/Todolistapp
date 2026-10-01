import os
import json
import pika

from dotenv import load_dotenv

load_dotenv()


RABBITMQ_HOST = os.getenv(
    "RABBITMQ_HOST",
    "localhost"
)

RABBITMQ_PORT = int(
    os.getenv(
        "RABBITMQ_PORT",
        "5672"
    )
)

RABBITMQ_USER = os.getenv(
    "RABBITMQ_USER",
    "guest"
)

RABBITMQ_PASSWORD = os.getenv(
    "RABBITMQ_PASSWORD",
    "guest"
)

QUEUE_NAME = os.getenv(
    "RABBITMQ_QUEUE",
    "email_queue"
)


def publish_email(
    to_email: str,
    subject: str,
    body: str
):

    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )

    connection = pika.BlockingConnection(
        parameters
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "to": to_email,
        "subject": subject,
        "body": body
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()