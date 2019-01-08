import hashlib
import json
import math
import hashlib
from custom_cipher import CustomCipher

# Temporary Ledger initialization
from Crypto.PublicKey import RSA
from aes_cipher import AESCipher


class Node:
    def __init__(self, serial_key, key_file):
        self.cipher = CustomCipher()
        key, public_key, secret_key = self.cipher.init_keys(serial_key, key_file)
        self.secret_key = secret_key
        self.public_key = public_key
        self.key = key
        
        #print public_key
        #print secret_key
        
        # Temporary Ledger initialization
        aes_cipher = AESCipher()
        
        dev1_serial = "Device0001"
        dev1_serial_hash = hashlib.sha256(dev1_serial.encode()).digest()
        dev1_pub = aes_cipher.encrypt(RSA.importKey(open("device1-public.pem", "rb")).exportKey('PEM'), dev1_serial_hash)
        
        self.ledger = {
            dev1_serial: dev1_pub
        }
        # self.blockchain = []
    
    def encrypt(self, serial, message):
        if serial in self.ledger:
            public_key = self.ledger[serial]
            secret_key = hashlib.sha256(serial.encode()).digest()
            return self.cipher.encrypt(public_key, secret_key, message)
        
    def decrypt(self, message):
        return self.cipher.decrypt(message, self.key)
        
    def sign(self, data):
        signature = self.cipher.sign(self.key, data)
        return signature
        
    def verify(self, data, signature):
        return self.cipher.verify(self.public_key, self.secret_key, data, signature)

    def process_message(self, message):
        print message
        
class Device:
    def __init__(self, serial_key, key_file):
        self.cipher = CustomCipher()
        key, public_key, secret_key = self.cipher.init_keys(serial_key, key_file)
        self.secret_key = secret_key
        self.public_key = public_key
        self.key = key
        # self.blockchain = []
    
    def encrypt(self, serial, message):
        if serial in self.ledger:
            public_key = self.ledger[serial]
            secret_key = hashlib.sha256(serial.encode()).digest()
            return self.cipher.encrypt(public_key, secret_key, message)
        
    def decrypt(self, message):
        return self.cipher.decrypt(message, self.key)
    
    def sign(self, data):
        signature = self.cipher.sign(self.key, data)
        return signature
        
    def verify(self, data, signature):
        return self.cipher.verify(self.public_key, self.secret_key, data, signature)
