from websocket import create_connection
import json
ws = create_connection("ws://192.168.88.182:8000/analytics/?authorization=2c92efb60ed2a08209864159eb1c9be453587150")
i = 0

payment = {"type":"order_payment","data":[
    {"order_id":"1",
    "status":"Paid",
    "status_message":str("{}").format(i),
    "description": "payment_descri1ption"
    }]}

order = {"type":"order_draft","data":[
    {"order_id":"1",
    "status":"Success",
    "status_message":"status_message_order",
    "description": "order_description",
    "user_id": 1,
    "merchant_id":1,
    
    }]}

while i < 1:
    
    ws.send(json.dumps(order))
    i += 1
    
ws.recv()

ws.close()