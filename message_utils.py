import datetime
import json

def gen_message(type, sender, slot1):
    message = {
        "sender": sender,
        "type": type,
        "slot1": slot1,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return json.dumps(message)

def load_message(dec):
    return json.loads(dec)

def display_message(message):
    print('Message Contents')
    print('Sender: ' + message['sender'])
    print('Type: ' + message['type'])
    print('Slot1: ' + message['slot1'])
    print('Timestamp: ' + message['timestamp'])