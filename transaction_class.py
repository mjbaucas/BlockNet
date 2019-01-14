import datetime

class Transaction:
    def __init__(self, type, device_serial, public_key):
        self.type = type
        self.device_serial = device_serial
        self.public_key = public_key
        self.timestamp = datetime.datetime.now().isoformat()
    
