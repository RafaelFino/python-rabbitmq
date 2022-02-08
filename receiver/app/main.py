#!/usr/bin/env python
import pika, sys, os
from time import sleep

for i in range(5):
    print(" [*] Waiting to start...")
    sleep(1)

print(" [*] Connecting...")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', 
    credentials=pika.PlainCredentials('user', 'password')))


print(" [*] Getting channel...")
channel = connection.channel()
channel.queue_declare(queue='default-queue')

def callback(ch, method, properties, body):
    print(" [<] Received %r" % body)

print(" [*] Setting receiver...")
channel.basic_consume(queue='default-queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages...')
channel.start_consuming()

print(" [X] Stop!")