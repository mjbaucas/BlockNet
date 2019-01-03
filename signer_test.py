from key_cipher import AESCipher

if __name__ == "__main__":
    private_key = "STRING"
    cipher = AESCipher()

    enc = cipher.encrypt("This message", private_key)
    print(enc)
    dec = cipher.decrypt(enc, private_key)
    print(dec)
