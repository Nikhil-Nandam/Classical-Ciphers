# Import socket module
import socket
import time
from random import randint


def create_key(plain_text):
    key = []
    while len(key) < len(plain_text):
        integer = randint(97, 122)
        if chr(integer) in key:
            continue
        else:
            key.append(chr(integer))

    return ''.join(key)


def encrypt(plain_text, secret_key):
    cipher_text = []
    for i in range(len(plain_text)):
        char = chr(((ord(plain_text[i]) + ord(secret_key[i]) - 97 * 2) % 26) + 97)
        cipher_text.append(char)

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
secret_key = create_key(plain_text)
print('Secret Key:', secret_key)
print(encrypt(plain_text, secret_key))

s.send(encrypt(plain_text, secret_key).encode())
time.sleep(0.5)
s.send(secret_key.encode())
print("Message sent")
s.close()
