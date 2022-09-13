from .connection import Connection
from django_thread import Thread
from .models import *
import ast


class SimpleSender(Thread):

    def __init__(self, destiny, json_encoded):
        Thread.__init__(self)
        self.connection = Connection().start_connection()
        self.destiny = destiny
        self.json_encoded = json_encoded

    def run(self):
        channel = self.connection.channel()
        channel.basic_publish(exchange='',
                              routing_key=self.destiny,
                              body=self.json_encoded)
        self.connection.close()


class SimpleConsumer(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.connection = Connection().start_connection()

    def callback(ch, queue, method, properties, body):
        segment = body.decode('utf-8')
        json = ast.literal_eval(segment)
        contact, created = Contact.objects.get_or_create(
            name=json['SENDER'])
        contact.save()
        new_message = ContactMessage.objects.create(
            message=json['MESSAGE'],
            origin=json['SENDER'],
            contact=contact)
        new_message.save()

    def run(self):
        channel = self.connection.channel()
        channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()


class PubSubSender(Thread):

    def __init__(self, group, json_encoded):
        Thread.__init__(self)
        self.connection = Connection().start_connection()
        self.group = group
        self.json_encoded = json_encoded

    def run(self):
        channel = self.connection.channel()
        channel.basic_publish(exchange=self.group,
                              routing_key='', body=self.json_encoded)
        self.connection.close()


class PubSubConsumer(Thread):

    def __init__(self, exchange):
        Thread.__init__(self)
        self.exchange = exchange
        self.connection = Connection().start_connection()

    def callback(ch, queue, method, properties, body):
        segment = body.decode('utf-8')
        json = ast.literal_eval(segment)
        group, created = Group.objects.get_or_create(group=json['GROUP'])
        group.save()
        new_message = GroupMessage.objects.create(
            message=json['MESSAGE'], origin=json['SENDER'], group=group)
        new_message.save()

    def run(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.exchange, queue=queue_name)
        channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()
