import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from aes_cipher import AESCipher
from rsa_cipher import RSACipher


class CustomCipher:
	def __init__(self):
		self.aes_cipher = AESCipher()
		self.rsa_cipher = RSACipher()
		
	def gen_keys(self, secret_key):
		key = self.rsa_cipher.gen_key()
		
		public_key = key.publickey().exportKey('PEM')
		secret_key = hashlib.sha256(secret_key.encode()).digest()
		public_key = self.aes_cipher.encrypt(public_key, secret_key)
		return key, public_key, secret_key
		
	def encrypt(self, public_key, secret_key, message):
		dec_public_key = self.aes_cipher.decrypt(public_key, secret_key)
		key = RSA.importKey(dec_public_key) 
		return key.encrypt(message, 'x')

	def decrypt(self, enc_message, key):
		return self.rsa_cipher.decrypt(key, enc_message)
		
	def sign(self, key, data):
		return self.rsa_cipher.sign(key, data)
	
	def verify(self, public_key, secret_key, data, signature):
		dec_public_key = self.aes_cipher.decrypt(public_key, secret_key)
		key = RSA.importKey(dec_public_key) 
		return self.rsa_cipher.verify(key, data, signature)
