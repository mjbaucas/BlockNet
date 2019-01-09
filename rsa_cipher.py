from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

import zlib
import base64

class RSACipher:
	def __init__(self):
		self.base = 4096
		self.e = 65537
		self.rand = Random.new().read
		
	def gen_key(self):
		key = RSA.generate(self.base, e=self.e)
		return key
	
	def encrypt(self, public_key, data):
		if public_key.can_encrypt():
			rsa_key = PKCS1_OAEP.new(public_key)
			
			data = zlib.compress(data)
			
			chunksize = ((self.base/16) - 42)
			offset = 0
			end = False
			encrypted = ""
			
			while not end:
				chunk = data[offset:offset + chunksize]
				
				if len(chunk) % chunksize != 0:
					end = True
					chunk += " " * (chunksize - len(chunk))
				encrypted += rsa_key.encrypt(chunk)
				offset += chunksize
			
			return True, base64.b64encode(encrypted)
		return False, ''
	
	def decrypt(self, key, data):
		if key.has_private():
			rsa_key = PKCS1_OAEP.new(key)
			
			data = base64.b64decode(data)
			
			chunksize = ((self.base/16))
			offset = 0
			decrypted = ""
			
			while offset < len(data):
				chunk = data[offset:offset + chunksize]
				decrypted += rsa_key.decrypt(chunk)
				offset += chunksize
			
			return True, zlib.decompress(decrypted)
		return False, ''
		
	def sign(self, key, data):
		hash_data = SHA256.new(data.encode()).digest()
		return key.sign(hash_data,'')
		
	def verify(self, public_key, data, signature):
		hash_data = SHA256.new(data.encode()).digest()
		return public_key.verify(hash_data, signature)
