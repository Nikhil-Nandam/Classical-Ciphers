# Import socket module
import socket
import time
from random import randint


def create_key() -> str:
    key = []
    while len(key) < 26:
        random_int = randint(97, 122)
        if chr(random_int) in key:
            continue
        key.append(chr(random_int))

    return ''.join(key)


def encrypt(plain_text: str, key: str) -> str:
    cipher_text = []
    for i in range(len(plain_text)):
        position = ord(plain_text[i]) - 97
        cipher_text.append(key[position])

    return ''.join(cipher_text)


s = socket.socket()
port = 12345
try:
    s.connect(('127.0.0.1', port))
except ConnectionRefusedError:
    print("Server refused to connect!!")
    exit()

print('Enter Plain Text: ')
plain_text = input().strip()
print('Generating Secret Key...')
secret_key = create_key()
print('Secret Key:', secret_key)
print('Encrypted text:', encrypt(plain_text, secret_key))

s.send(encrypt(plain_text, secret_key).encode())
time.sleep(0.5)
s.send(secret_key.encode())
print("Message sent")
s.close()
