import hashlib
import json
import math
import hashlib
import base64
import ast

from custom_cipher import CustomCipher
from chain_class import Chain

from Crypto.PublicKey import RSA


# Temporary Ledger initialization
from aes_cipher import AESCipher


class Node:
    def __init__(self, serial_key, key_file):
        self.cipher = CustomCipher()
        key, public_key, secret_key = self.cipher.init_keys(serial_key, key_file)
        self.secret_key = secret_key
        self.public_key = public_key
        self.serial_key = serial_key
        self.key = key
        
        #print public_key
        #print secret_key
        
        # Ledger initialization
        aes_cipher = AESCipher()
        
        dev1_serial = "Device0001"
        dev1_serial_hash = hashlib.sha256(dev1_serial.encode()).digest()
        dev1_pub = aes_cipher.encrypt(RSA.importKey(open("device1-public.pem", "rb")).exportKey('PEM'), dev1_serial_hash)
        
        self.blockchain = Chain()
        self.blockchain.gen_next_block(hashlib.sha256("DeviceAccessBlock1".encode()).digest(), [{"Serial": dev1_serial, "PubKey": dev1_pub}])
        self.ledger = self.blockchain.output_ledger()
        
    def encrypt(self, serial, message):
        if serial in self.ledger:
            public_key = self.ledger[serial]
            secret_key = hashlib.sha256(serial.encode()).digest()
            return self.cipher.encrypt(public_key, secret_key, message)

    def process_message(self, message):
        message = ast.literal_eval(message)
        if all(x in message for x in ["type", "serial"]):
            if message["type"] == "access":
                return self.process_access_message(message["serial"])
        return None
    
    def sign(self, key, data):
        signature = self.cipher.sign(key, data)
        return signature
        
    def process_access_message(self, serial):
        aes_cipher = AESCipher()
        
        if serial in self.ledger:
            data = json.dumps({"type": "response", "serial": self.serial_key, "status": "approved"})
            signature = self.sign(self.key, data)
            enc_data = aes_cipher.encrypt(data, hashlib.sha256(self.serial_key.encode()).digest())
            message = json.dumps({"message": enc_data, "signature": signature, "serial": self.serial_key})
            enc_message = self.encrypt(serial, message)
            return enc_message
        return None
    
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
        
    def process_network_message(self, data):
        aes_cipher = AESCipher()
                
        if self.is_paired:
            signature = self.sign(self.key, data)
            enc_data = aes_cipher.encrypt(data, hashlib.sha256(self.serial_key.encode()).digest())
            message = json.dumps({"message": enc_data, "signature": signature, "serial": self.serial_key})
            enc_message = self.encrypt(self.network_serial_key, self.network_public_key, message)
            return enc_message
        return None
    
    def read_network_message(self, message):
        aes_cipher = AESCipher()
        
        if self.is_paired:
            message = self.decrypt(message, self.key)
            message = ast.literal_eval(message)
            if all(x in message for x in ["message", "signature", "serial"]):
                serial = hashlib.sha256(message['serial'].encode()).digest()
                data = aes_cipher.decrypt(message["message"], serial)
                signature = message["signature"]
                if self.cipher.verify(self.network_public_key, serial, data, signature):
                    return data
        return None
