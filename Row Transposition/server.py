import socket


def get_order(secret_key: str) -> list:
    key_map, dictionary = {}, {}
    key_length = len(secret_key)
    for i in range(key_length):
        key_map[i] = secret_key[i]

    return sorted(key_map, key=lambda x: key_map[x])


def split(cipher_text, key_length) -> list:
    length = len(cipher_text) // key_length
    res = []
    for i in range(0, len(cipher_text), length):
        res.append(cipher_text[i : i + length])

    return res


def decrypt(cipher_text: str, secret_key: str) -> str:
    plain_text = []
    cipher_text_length = len(cipher_text)
    key_length = len(secret_key)
    order = get_order(secret_key)
    splits = split(cipher_text, key_length)
    order, splits = zip(*sorted(zip(order, splits)))
    for i in range(cipher_text_length // key_length):
        for j in range(key_length):
            plain_text.append(splits[j][i])

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