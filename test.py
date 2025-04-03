from crypto import Cipher

cipher = Cipher('key.bin')

encrypted = cipher.encrypt('test')
print(encrypted)
decrypted = cipher.decrypt(encrypted)
print(decrypted)