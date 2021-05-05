from websocket import create_connection
import json
ws = create_connection("ws://192.168.88.182:8000/analytics/?authorization=282571fa2626e75a9f4d84f5557d56d35fc22429")
# ws = create_connection("ws://167.86.115.50:8000/analytics/?authorization=b1b82511632d423c4f0ad6218546d26add873afa")
i = 0

payment = {"type":"order_payment","data":[
    {"order_id":"3",
    "status":"Paid",
    "status_message":'',
    "description": "payment_descri1ption"
    }]}

order = {'type': 'order_payment', 
'data':[ 
{'order_id': "1111", 'status': 'success', 'status_message': '#79 üçün draft yaradıldı', 'description': '', 'payment_status': 0, 'payment_method': 2, 'user_id': 21, 'merchant_id': 1,"point":1}]
}

while i < 1:
    
    ws.send(json.dumps(order))
    i += 1
    
ws.recv()

ws.close()