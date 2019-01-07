from custom_cipher import CustomCipher

if __name__ == "__main__":
	cipher = CustomCipher()
	key, pub, sec = cipher.gen_keys("test")
	
	test_data = "Hello World"
	sig = cipher.sign(key, test_data)
	print cipher.verify(pub, sec, test_data, sig)
