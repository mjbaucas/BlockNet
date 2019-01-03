import hashlib
import json
import math
from aes_cipher import AESCipher

network_key = hashlib.sha256("Network0001".encode()).digest()

class Node:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = hashlib.sha256(private_key.encode()).digest()
        self.cipher = AESCipher()
        self.ledger = {}
        self.whitelist = {}
        self.blacklist = []
        self.tx_power = -69 # Measured Power Assumed
        self.env_factor = 2 # Environmental Factor Assumed
        self.jurisdiction = 20
        self.network_key = network_key
        # self.blockchain = []
    
    def encrypt(self, message, key):
        if key:
            return self.cipher.encrypt(message, key)
        else:     
            return self.cipher.encrypt(message, self.public_key)
        
    def decrypt(self, message, key):
        if key:
            return self.cipher.decrypt(message, key)
        else:        
            return self.cipher.decrypt(message,self.public_key)
        
    def add_to_ledger(self, users):
        if isinstance(users, dict):
            for key, item in users.items():
                self.ledger[key] = item

    def add_to_whitelist(self, device, distance, energy):
        self.whitelist[device] = [distance, energy]

    def process_message(self, message):
        temp_list = message.split("+9087+")
        if len(temp_list) != 2:
            print("MESSAGE BLOCKED - FORMAT")
            return False
        if not temp_list[0] in self.ledger:
            print("MESSAGE BLOCKED - LEDGER: " + temp_list[0])
            return False

        pub_key = hashlib.sha256(self.ledger[temp_list[0]].encode()).digest()
        dec = json.loads(self.decrypt(temp_list[1], pub_key))

        distance = self.get_distance(dec["rssi"])
        if distance > self.jurisdiction:
            print("MESSAGE BLOCKED - DISTANCE: " + temp_list[0])
            return False

        if dec["type"] == "access":
            if temp_list[0] in self.blacklist:
                print("ACCESS BLOCKED - BLACK LIST: " + temp_list[0])
                return False
           
            if temp_list[0] not in self.whitelist:
                print("ACCESS GRANTED: " + temp_list[0])
                self.add_to_whitelist(temp_list[0], distance, dec["res_energy"])
            else:
                print("ACCESS REDUNDANT: " + temp_list[0])

        elif dec["type"] == "send_data":
            if all(device in self.whitelist for device in [temp_list[0], dec["destination"]]) and not any(device in self.blacklist for device in [temp_list[0], dec["destination"]]): 
                dist_1 = self.get_distance(dec["rssi"])
                dist_2 = self.whitelist[dec["destination"]][0]
                res_energy = self.whitelist[temp_list[0]][1]
                
                # Assume that every meter requires 1 unit of energy to send
                # Assume that the maximum possible distance between the two devices is the actual distance
                max_dist = dist_1 + dist_2
                if max_dist > res_energy:
                    print("REQUEST BLOCKED - ENERGY: " + temp_list[0])                    
                print("TRANSACTION GRANTED: " + temp_list[0] + " to " + dec["destination"] )
            else:
                if temp_list[0] not in self.whitelist or temp_list[0] in self.blacklist:
                    print("REQUEST BLOCKED - SOURCE: " + temp_list[0])
                if dec["destination"] not in self.whitelist or dec["destination"] in self.blacklist:
                    print("REQUEST BLOCKED - DESTINATION: " + dec["destination"])

    def get_distance(self, rssi):
        return math.pow(10, (float(self.tx_power - rssi)) / (10 * self.env_factor))

class Device:
    def __init__(self, private_key, id):
        self.id = id
        self.private_key = private_key
        self.public_key = hashlib.sha256(private_key.encode()).digest()
        self.cipher = AESCipher()
        self.node_key = ""
        self.network_key = network_key
        # self.blockchain = []
    
    def is_granted_access(self):
        return self.node_key != ""
    
    def set_node_key(self, pub_key):
        self.node_key = pub_key

    def encrypt(self, message, key):
        if key:
            return self.cipher.encrypt(message, key)
        else:     
            return self.cipher.encrypt(message, self.public_key)
        
    def decrypt(self, message, key):
        if key:
            return self.cipher.decrypt(message, key)
        else:        
            return self.cipher.decrypt(message,self.public_key)
    
    def dig_sign(self, message):
        return self.id + "+9087+" + message

