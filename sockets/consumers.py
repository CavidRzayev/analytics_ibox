from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer,WebsocketConsumer
import json



class DataPasing:
    def __init__(self,*args,**kwargs):
        self.__dict__.update(args)
        self.data = self.__dict__

class AnalyticsConsumers(WebsocketConsumer,DataPasing):
    
    STATUS = (
        (1,''),
        (2,),
        (3,),
        (4,),
        (5,),
        (6,),
        (7,),
        (8,),
    )

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.dumps(text_data)
        message = json.loads(text_data_json)
        print(message)
        if self.scope['auth'] == True:
            self.send(text_data=json.dumps({
                'data': "Authorization success"
            }))
        else:
            self.send(text_data=json.dumps({
                'error': "Authorization error"
            }))