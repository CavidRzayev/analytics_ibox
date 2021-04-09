from websocket import create_connection
import json
ws = create_connection("ws://192.168.88.232:8000/analytics/?authorization=2c92efb60ed2a08209864159eb1c9be453587150")
i = 0

payment = {"type":"order_payment","data":[
    {"order_id":"3",
    "status":"Paid",
    "status_message":str("{}").format(i),
    "description": "payment_description"
    }]}

order = {"type":"order_checkout","data":[
    {"order_id":"2",
    "status":"Success",
    "status_message":"status_message_order",
    "description": "order_description",
    
    }]}

while i < 200:
    
    ws.send(json.dumps(payment))
    i += 1
    
ws.recv()

ws.close()