import pika
import logging

class MQConnection:
    def __init__(self) -> None:
        self.connection = None
        self.connected = False

    def Connect(self, user, passwd):
        logging.debug("Connecting to MQ...") 
        self.connected = False
        self.connection = None
        ret = None

        try:            
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='mq', 
                credentials=pika.PlainCredentials(user, passwd)))
            self.connected = True
            
            ret = "Connection to MQ established"
            logging.info(ret)
            
        except pika.exceptions.AMQPConnectionError as Err:
            ret = "pika.exceptions: {}".format(Err)
            logging.error(ret)
            raise Exception(ret)
        
        except Exception as Err:
            ret = "Exception: {}".format(Err)
            logging.error(ret)
            raise Exception(ret)

        return ret
    
    def Disconnect(self):
        logging.debug("Disconnecting from MQ...") 

        if self.connection == None:
            return "Already disconnected"
        
        try:            
            self.connection.close()
            self.connection = None
            self.connected = False

            ret = "Connection to MQ closed"
        except Exception as Err:
            ret = "Exception: {}".format(Err)
            logging.error(ret)
            raise Exception(ret)
        
        return ret
         

    def DeclareQueue(self, name):
        logging.debug("Declaring queue {0}".format(name))    
        ret = None
        
        if self.connection == None:
            ret = "Not connected"
            raise Exception(ret)
        
        try:                        
            channel = self.connection.channel()
            channel.queue_declare(queue=name, durable=True)

            ret = "Queue {0} declared".format(name)
        except Exception as Err:
            ret = "Exception: {}".format(Err)
            raise Exception(ret)

        return ret
        
    
    def Send(self, queue, msg):
        logging.debug("Sending message to queue...") 
        ret = None
        
        if self.connection == None:
            ret = "Not connected"
            raise Exception(ret)
        
        try:
            channel = self.connection.channel()
            
            channel.basic_publish(exchange='', 
                routing_key=queue, 
                body=msg)
            
            channel.close()
            
            ret = "message sent to {}".format(queue)

        except Exception as Err:
            ret = "Exception: {}".format(Err)
            raise Exception(ret)
        
        return ret
    
