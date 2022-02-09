import pika, sys, os
from time import sleep

def connect():
    connection = None    
    print(" [*] Trying connect...")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            credentials=pika.PlainCredentials('user', 'password')))

        print(" [#] Connected! ")
        connected = True
    except pika.exceptions.AMQPConnectionError as Err:
        print(" [X] Error: {0} ".format(Err))
        return None
    except:
        print(" [X] Error!")

    return connection

conn = None

print(" [*] Starting...")

while conn == None:
    conn = connect()
    sleep(1)

print(" [*] Getting channel...")
channel = conn.channel()
channel.queue_declare(queue='default-queue')

def callback(ch, method, properties, body):
    print(" [<] Received %r" % body)

print(" [*] Setting receiver...")
channel.basic_consume(queue='default-queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages...')
channel.start_consuming()

print(" [*] Clossing channel...")
channel.close()

print(" [*] Closing connection...")
conn.close();

print(" [X] Stop!")