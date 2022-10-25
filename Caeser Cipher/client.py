# Import socket module
import socket
import time


def encrypt(plain_text, secret_key):
    key = int(secret_key)
    cipher_text = []
    for char in plain_text:
        cipher_char = chr(((ord(char) + key - 97) % 26) + 97)
        cipher_text.append(cipher_char)

    # print(cipher_text)
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
print('Enter Secret Key: ')
secret_key = input().strip()

s.send(encrypt(plain_text, secret_key).encode())
time.sleep(0.5)
s.send(secret_key.encode())
print("Message sent")
s.close()
