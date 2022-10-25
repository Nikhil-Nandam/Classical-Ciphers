import socket


def decrypt(cipher_text: str, secret_key: str) -> str:
    plain_text = []
    for i in range(len(cipher_text)):
        position = secret_key.index(cipher_text[i])
        plain_text.append(chr(position + 97))

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
    print("Secret Key: " + secret_key)
    print("Decrypted message: " + decrypt(cipher_text, secret_key))
