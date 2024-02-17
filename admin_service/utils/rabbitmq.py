import pika
from admin_service.config import settings
import json
from admin_service.models_choices import EmailSubject


class RabbitMQPublisher:
    def __init__(self):
        self.queue_name = settings.rabbitmq_queue
        self.credentials = pika.PlainCredentials(
            settings.rabbitmq_user, settings.rabbitmq_password.get_secret_value()
        )
        self.parameters = pika.ConnectionParameters(
            settings.rabbitmq_host,
            settings.rabbitmq_port,
            settings.rabbitmq_vhost,
            self.credentials,
        )
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    @staticmethod
    def create_message(email: str, subject: EmailSubject) -> bytes:
        return json.dumps(
            {
                "email": email,
                "subject": subject.value,
            }
        ).encode("utf-8")

    def publish(self, email: str, subject: EmailSubject):
        message_json = self.create_message(email, subject)
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=message_json
        )
        print(f" [x] Sent {message_json}")

    def close(self):
        self.connection.close()
