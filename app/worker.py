import json
import pika

from app.services.email import send_email

import os

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


def callback(
    ch,
    method,
    properties,
    body
):

    message = json.loads(
        body.decode()
    )

    print(
        "Sending email to:",
        message["to"]
    )


    try:

        send_email(

            to_email=message["to"],

            subject=message["subject"],

            body=message["body"]
        )

        print(
            "Email sent successfully"
        )


        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )


    except Exception as error:

        print(
            "Email failed:",
            error
        )

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )


channel.basic_qos(
    prefetch_count=1
)


channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback
)


print(
    "RabbitMQ email worker started..."
)


channel.start_consuming()