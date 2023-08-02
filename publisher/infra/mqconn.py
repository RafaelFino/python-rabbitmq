import pika
import logging

class MQConnection:
    def __init__(self) -> None:
        self.connection = None
        self.connected = False

    def Connect(self, user, passwd) -> bool:
        self.connected = False
        self.connection = None

        try:
            logging.debug("Connecting to MQ...") 
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='mq', 
                credentials=pika.PlainCredentials(user, passwd)))
            self.connected = True

            logging.info("Connection to MQ established")
            
        except pika.exceptions.AMQPConnectionError as Err:
            logging.error("pika.exceptions: {}".format(Err)) 
        except Exception as Err:
            logging.error("Exception: {}".format(Err))        

        return self.connected
    
    def Disconnect(self) -> bool:
        if self.connection == None:
            return True
        
        try:
            logging.debug("Disconnecting from MQ...") 
            self.connection.close()
            self.connection = None
            self.connected = False

            logging.info("Connection to MQ closed")
        except Exception as Err:
            logging.error("Exception: {}".format(Err))
            return False
        
        return True
         

    def DeclareQueue(self, name) -> bool:
        if self.connection == None:
            return False
        
        try:
            logging.debug("Declaring queue {0}".format(name))    
            channel = self.connection.channel()
            channel.queue_declare(queue='default-queue')        

            logging.info("Queue {0} declared".format(name))

            return True

        except Exception as Err:
            logging.error("Exception: {}".format(Err))

        return False
    
    def Send(self, queue, msg) -> bool:
        if self.connection == None:
            return False
        
        try:
            channel = self.connection.channel()
            
            channel.basic_publish(exchange='', 
                routing_key=queue, 
                body=msg)
            
            channel.close()
            
            logging.debug("[{0}] sending -> [{1}]".format(queue, msg))

        except Exception as Err:
            logging.error("Exception: {}".format(Err))
            return False

        
        return True
    
