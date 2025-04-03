from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


class Cipher:
    def __init__(self, key_file: str):
        with open(key_file, "rb") as kf:
            self.key = kf.read()
            self.hex_block_size = AES.block_size * 2

    def cipher(self, iv=None):
        return AES.new(self.key, AES.MODE_CBC, iv=iv)

    def encrypt(self, raw: str) -> str:
        cipher = self.cipher()
        c = cipher.encrypt(pad(raw.encode(), AES.block_size))
        iv, c = tuple(x.hex() for x in (cipher.iv, c))
        return iv + c

    def decrypt(self, ivc: str) -> str:
        iv = bytes.fromhex(ivc[:self.hex_block_size])
        c = bytes.fromhex(ivc[self.hex_block_size:])
        return unpad(self.cipher(iv).decrypt(c), AES.block_size).decode()
