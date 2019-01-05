from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random

class RSACipher:
	def __init__(self):
		self.base = 2048
		self.rand = Random.new().read
		
	def gen_keys(self, serial_key):
		key = RSA.generate(self.base, serial_key)
		private_key = key.export_key()
		
		public_key = key.public_key().export_key()
		return private_key, public_key, key
	
	def encrypt(self, public_key, data):
		if public_key.can_encrypt() and public_key.has_private():
			return True, public_key.encrypt(data, 32)
		return False, ''
	
	def decrypt(self, private_key, data):
		return private_key.decrypt(data)
		
	def sign(self, key, data):
		hash_data = SHA256.new(data.encode()).digest()
		return key.sign(hash_data,'')
		
	def verify(self, public_key, data, signature):
		hash_data = SHA256.new(data.encode()).digest()
		return public_key.verify(hash_data, signature)
