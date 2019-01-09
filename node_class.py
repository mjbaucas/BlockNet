import hashlib
import json
import math
import hashlib
import base64

from custom_cipher import CustomCipher

from Crypto.PublicKey import RSA

# Temporary Ledger initialization
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

    def process_message(self, message):
        print message
        
    def read_message(self, message):
        aes_cipher = AESCipher()
        
        message = self.cipher.decrypt(message, self.key)
        message = json.loads(message)
        if all(x in message for x in ["message", "signature", "serial"]):
            data = message["message"]
            signature = message["signature"]
            serial = message["serial"]
            secret = hashlib.sha256(serial.encode()).digest()
            if serial in self.ledger:
                dec_data = aes_cipher.decrypt(data, secret)
                pub_key = self.ledger[serial]
                if self.cipher.verify(pub_key, secret, dec_data, signature):
                    return dec_data
        return None
        
class Device:
    def __init__(self, serial_key, key_file):
        self.cipher = CustomCipher()
        key, public_key, secret_key = self.cipher.init_keys(serial_key, key_file)
        self.secret_key = secret_key
        self.public_key = public_key
        self.serial_key = serial_key
        self.key = key
                
        self.is_paired = False

    def pair_device(self, network_serial_key, network_file):
        network_key, network_public_key, network_secret_key = self.cipher.init_keys(network_serial_key, network_file)
        self.network_secret_key = network_secret_key
        self.network_public_key = network_public_key
        self.network_serial_key = network_serial_key
        self.network_key = network_key
        
        self.is_paired = True
        
    def encrypt(self, serial, public_key, message):
        secret_key = hashlib.sha256(serial.encode()).digest()
        return self.cipher.encrypt(public_key, secret_key, message)
    
    def decrypt(self, message, key):
        return self.cipher.decrypt(message, key)
    
    def sign(self, key, data):
        signature = self.cipher.sign(key, data)
        return signature
        
    def verify(self, data, signature):
        return self.cipher.verify(self.public_key, self.secret_key, data, signature)

    def process_network_message(self, data):
        aes_cipher = AESCipher()
                
        if self.is_paired:
            signature = self.sign(self.key, data)
            enc_data = aes_cipher.encrypt(data, hashlib.sha256(self.serial_key.encode()).digest())
            message = json.dumps({"message": enc_data, "signature": signature, "serial": self.serial_key})
            enc_message = self.encrypt(self.network_serial_key, self.network_public_key, message)
            return enc_message
        return None
    
    def read_message(self, message):
        aes_cipher = AESCipher()
        
        if self.is_paired:
            message = self.decrypt(message, self.key)
            if all(x in message for x in ["message", "signature", "serial"]):
                data = message["message"]
                signature = message["signature"]
                if self.verify(data, signature):
                    print aes_cipher.decrypt(message, self.public_key)
                    return "YES"
        return None
