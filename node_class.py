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
        print message
        
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
        if self.cipher != None:
            hashed_message = hashlib.sha256(message.encode()).digest()
            return True, self.encrypt(hashed_message, self.private_key)
        return False, ""
        
