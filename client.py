from websocket import create_connection
import json
#ws = create_connection("ws://192.168.88.182:8000/analytics/?authorization=a7ca9e4292d457b452525471b5ff8c63e7e609be")
ws = create_connection("ws://monitoring.iboxapp.az//analytics/?authorization=47174b9ff677f9e5bf97f74de5940fab670117d1")
i = 0

payment = {"type":"order_payment","data":[
    {"order_id":"3",
    "status":"Paid",
    "status_message":'',
    "description": "payment_descri1ption"
    }]}

order = {'type': 'order_draft', 
'data':[ 
{'order_id': "3", 'status': 'success', 'status_message': '#79 üçün draft yaradıldı', 'description': '', 'payment_status': 0, 'payment_method': 1, 'user_id': 21, 'merchant_id': 1,"point":1}]
}


logging = {'type': 'realtime_logging', 
'data':[ 
{"status":"error","message":"test","content":'[{"id":1412,"name":"Test"},{"id":13,"order_id":"141"}]'}]
}

while i < 1:
    
    
    ws.send(json.dumps(order))
   
    i += 1
    # ws.send(json.dumps(order))
    
#ws.recv()

ws.close()
