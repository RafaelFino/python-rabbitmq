import pika
import datetime
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

for loop in range(100):
    print(" [*] Starting loop {0}".format(loop))  

    print(" [*] Getting channel...")
    channel = conn.channel()
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
conn.close()

print(" [X] Stop")