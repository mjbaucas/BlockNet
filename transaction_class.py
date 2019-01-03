import datetime

class Transaction:
    def __init__(self, type, slot1, slot2):
        self.type = type
        self.slot1 = slot1
        self.slot2 = slot2
        self.timestamp = datetime.datetime.now().isoformat()
    
