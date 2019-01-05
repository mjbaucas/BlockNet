from aes_cipher import AESCipher
from rsa_cipher import RSACipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class CustomCipher:
	def __init__(self):
		self.aes_cipher = AESCipher()
		self.rsa_cipher = RSACipher()
		
	def gen_keys(self, secret_key):
		key = self.rsa_cipher.gen_key()
		
		public_key = key.publickey().exportKey('PEM')
		private_key = key.exportKey('PEM')
		
		enc_public_key = self.aes_cipher.encrypt(public_key, secret_key)
		print(enc_public_key)
		dec_public_key = self.aes_cipher.decrypt(enc_public_key, secret_key)
		print(dec_public_key)
		
		test_key = RSA.importKey(dec_public_key)
		enc_message = test_key.encrypt("Hello World", 'x')
		print(enc_message)
		print self.rsa_cipher.decrypt(key, enc_message)
		
		
