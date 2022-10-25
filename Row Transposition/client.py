# Import socket module
import socket
import time


def get_order(secret_key: str) -> list:
    key_map, dictionary = {}, {}
    key_length = len(secret_key)
    for i in range(key_length):
        key_map[i] = secret_key[i]

    return sorted(key_map, key=lambda x: key_map[x])


def append_chars(plain_text: str, key_length: int) -> str:
    plain_text_length = len(plain_text)
    extra_chars_count = 0 if plain_text_length % key_length == 0 \
        else key_length - (plain_text_length % key_length)
    extra_chars = [chr(i) for i in range(123 - extra_chars_count, 123)]
    return plain_text + ''.join(extra_chars)


def encrypt(plain_text: str, secret_key: str) -> str:
    order = get_order(secret_key)
    key_length = len(secret_key)
    plain_text = append_chars(plain_text, key_length)
    dictionary = {}
    for i in range(len(plain_text)):
        dict_key = i % key_length
        if dict_key in dictionary:
            dictionary[dict_key].append(plain_text[i])
        else:
            dictionary[dict_key] = [plain_text[i]]

    cipher_text = []
    for index in order:
        cipher_text.append(''.join(dictionary[index]))

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
print(encrypt(plain_text, secret_key))
s.send(encrypt(plain_text, secret_key).encode())
time.sleep(0.5)
s.send(secret_key.encode())
print("Message sent")
s.close()
