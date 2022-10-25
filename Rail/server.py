import socket
import math


def decrypt(cipher_text: str) -> str:
    length = len(cipher_text)
    plain_text = []
    for i in range(length // 2):
        plain_text.append(cipher_text[i])
        # try:
        plain_text.append(cipher_text[i + (math.ceil(length / 2))])
        # except IndexError:
        #     pass

    if length % 2 != 0:
        plain_text.append(cipher_text[length // 2])
    return ''.join(plain_text)

s = socket.socket()
port = 12345
s.bind(('', port))
print("socket bound to " + str(port))

while True:
    s.listen(5)
    print("socket is listening")
    connection, address = s.accept()
    print('Got connection from', address)

    cipher_text = connection.recv(1024).decode()
    secret_key = connection.recv(1024).decode()

    print("Encrypted message (Received): " + cipher_text)
    print("Decrypted message: " + decrypt(cipher_text))
