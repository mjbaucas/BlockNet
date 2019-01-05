import hashlib
import json
import math
from rsa_cipher import RSACipher

network_key = hashlib.sha256("Network0001".encode()).digest()

class Node:
    def __init__(self, serial_key):
        self.cipher = RSACipher()
        private_key, public_key, key = self.cipher.gen_keys(serial_key)
        self.private_key = private_key
        self.public_key = public_key
        self.key = key
        
        print public_key
        print private_key
        self.ledger = {}
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
        
class Device:
    def __init__(self, serial_key, id):
        self.cipher = RSACipher()
        private_key, public_key, key = self.cipher.gen_keys(serial_key)
        self.private_key = private_key
        self.public_key = public_key
        self.key = key
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
            return self.cipher.decrypt(message,self.private_key)
    
    def sign(self, message, key):
        if key:
            return self.cipher.sign(message, key)
        else:        
            return self.cipher.sign(message,self.private_key)
        
