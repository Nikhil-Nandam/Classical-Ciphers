# Import socket module
import socket
import time


def encrypt(plain_text):
    evens = [plain_text[i] for i in range(0, len(plain_text), 2)]
    odds = [plain_text[i] for i in range(1, len(plain_text), 2)]
    return ''.join(evens) + ''.join(odds)


s = socket.socket()
port = 12345
try:
    s.connect(('127.0.0.1', port))
except ConnectionRefusedError:
    print("Server refused to connect!!")
    exit()

print('Enter Plain Text: ')
plain_text = input().strip()
# print('Generating Secret Key...')
# secret_key = create_key(plain_text)
# print('Secret Key:', secret_key)
print('Encrypted text:', encrypt(plain_text))

s.send(encrypt(plain_text).encode())
time.sleep(0.5)
# s.send(secret_key.encode())
print("Message sent")
s.close()
