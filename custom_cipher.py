import hashlib

from Crypto.PublicKey import RSA

from aes_cipher import AESCipher
from rsa_cipher import RSACipher


class CustomCipher:
	def __init__(self):
		self.aes_cipher = AESCipher()
		self.rsa_cipher = RSACipher()
		
	def init_keys(self, secret_key, key_file):
		key = RSA.importKey(open(key_file, "rb"))
		
		public_key = key.publickey().exportKey('PEM')
							
		secret_key = hashlib.sha256(secret_key.encode()).digest()
		public_key = self.aes_cipher.encrypt(public_key, secret_key)
		return key, public_key, secret_key
		
	def gen_keys(self, secret_key, key_file):
		key = self.rsa_cipher.gen_key()
		
		public_key = key.publickey().exportKey('PEM')
		private_key = key.exportKey('PEM')
							
		secret_key = hashlib.sha256(secret_key.encode()).digest()
		public_key = self.aes_cipher.encrypt(public_key, secret_key)
		return key, public_key, secret_key
	
	def gen_key_file(self, file_name):
		with open(file_name + "-private.pem", "w") as priv_file:
			priv_file.write("{}".format(private_key))
					
		with open(file_name + "-public.pem", "w") as pub_file:
			pub_file.write("{}".format(public_key))
		
	def encrypt(self, public_key, secret_key, message):
		dec_public_key = self.aes_cipher.decrypt(public_key, secret_key)
		key = RSA.importKey(dec_public_key)
		result, encrypted = self.rsa_cipher.encrypt(key, message)
		return encrypted

	def decrypt(self, enc_message, key):
		result, decrypted = self.rsa_cipher.decrypt(key, enc_message)
		return decrypted
		
	def sign(self, key, data):
		return self.rsa_cipher.sign(key, data)
	
	def verify(self, public_key, secret_key, data, signature):
		dec_public_key = self.aes_cipher.decrypt(public_key, secret_key)
		key = RSA.importKey(dec_public_key) 
		return self.rsa_cipher.verify(key, data, signature)
