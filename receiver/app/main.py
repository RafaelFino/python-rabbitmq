import pika, sys, os
from time import sleep
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def connect():
    connection = None    
    logging.info(" [*] Trying connect...")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', 
            credentials=pika.PlainCredentials('user', 'password')))

        logging.info(" [#] Connected! ")
        connected = True
    except pika.exceptions.AMQPConnectionError as Err:
        logging.info(" [X] Error: {0} ".format(Err))
        return None
    except:
        logging.info(" [X] Error!")

    return connection

conn = None

logging.info(" [*] Starting...")

while conn == None:
    conn = connect()
    sleep(1)

logging.info(" [*] Getting channel...")
channel = conn.channel()
channel.queue_declare(queue='filona-da-hora')

def callback(ch, method, properties, body):
    logging.info(" [<] Received -> {0}".format(body.decode()))

logging.info(" [*] Setting receiver...")
channel.basic_consume(queue='filona-da-hora', on_message_callback=callback, auto_ack=True)    

logging.info(' [*] Waiting for messages...')
channel.start_consuming()

logging.info(" [*] Clossing channel...")
channel.close()

logging.info(" [*] Closing connection...")
conn.close();

logging.info(" [X] Stop!")