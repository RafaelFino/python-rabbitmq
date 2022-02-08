#!/usr/bin/env python
import pika
import datetime
from time import sleep

for i in range(5):
    print(" [*] Waiting to start...")
    sleep(1)

print(" [*] Connecting...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost', 
        credentials=pika.PlainCredentials('user', 'password')))



for loop in range(100):
    print(" [*] Starting loop {0}".format(loop))  

    print(" [*] Getting channel...")
    channel = connection.channel()
    channel.queue_declare(queue='default-queue')

    for i in range(20):
        print(" [>] Sending msg {0}".format(i))
        channel.basic_publish(exchange='', 
            routing_key='default-queue', 
            body='[{0}:{1}] my msg in {2}'.format(loop, i, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        sleep(1)

    print(" [*] Clossing channel...")
    channel.close()

print(" [*] Closing connection...")
connection.close()

print(" [X] Stop")