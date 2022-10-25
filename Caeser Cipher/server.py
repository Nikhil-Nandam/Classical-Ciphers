import socket

def decrypt(cipher_text: str, secret_key: str) -> str:
    plain_text = []
    key = int(secret_key)
    for char in cipher_text:
        plain_char = chr(((ord(char) - key - 97) % 26) + 97)
        plain_text.append(plain_char)

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
    print("Decrypted message: " + decrypt(cipher_text, secret_key))