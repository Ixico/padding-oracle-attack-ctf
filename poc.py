import base64
import binascii

from crypto import Cipher

cipher = Cipher('key.bin')


def oracle(ivc: str):
    try:
        cipher.decrypt(ivc)
        return True
    except ValueError:
        return False


def prepare_ivc(iv, c):
    prepared_iv = convert(iv, 'base64')
    prepared_c = convert(c, 'base64')
    return f'{prepared_iv}|{prepared_c}'


def convert_internal(b: bytes, form: str):
    if form == 'base64':
        return base64.b64encode(b).decode()
    if form == 'hex':
        return binascii.hexlify(b).decode()
    if form == 'bytearray':
        return bytearray(b)
    raise ValueError(f'Conversion error for form {form}.')


# form in (base64, hex, bytearray)
def convert(content, form: str):
    if type(content) == bytearray:
        return convert_internal(content, form)
    try:
        return convert_internal(base64.b64decode(content, validate=True), form)
    except binascii.Error:
        return convert_internal(binascii.unhexlify(content), form)


iv, c = cipher.encrypt('admin').split('|')
iv = convert(iv, 'bytearray')
c = convert(c, 'bytearray')
result = bytearray(16)
for i in range(15, -1, -1):
    curr_iv = iv[i]
    print(curr_iv)
    for j in range(256):
        iv[i] = j
        if oracle(prepare_ivc(iv, c)) and j != curr_iv:
            result[i] = j
            break
        result[i] = curr_iv
    print(result)
    break
