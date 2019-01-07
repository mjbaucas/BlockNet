import hashlib
import json
import math
import hashlib
from custom_cipher import CustomCipher

class Node:
    def __init__(self, serial_key):
        self.cipher = CustomCipher()
        key, public_key, secret_key = self.cipher.gen_keys(serial_key)
        self.secret_key = secret_key
        self.public_key = public_key
        self.key = key
        
        #print public_key
        #print secret_key
        self.ledger = {
            "NoDe0001": public_key, 
            "Device0002": public_key
        }
        # self.blockchain = []
    
    def encrypt(self, serial, message):
        if serial in self.ledger:
            public_key = self.ledger[serial]
            secret_key = hashlib.sha256(serial.encode()).digest()
            return self.cipher.encrypt(public_key, secret_key, message)
        
    def decrypt(self, message):
        return self.cipher.decrypt(message, self.key)
        
    def add_to_ledger(self, users):
        if isinstance(users, dict):
            for key, item in users.items():
                self.ledger[key] = item

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
        
