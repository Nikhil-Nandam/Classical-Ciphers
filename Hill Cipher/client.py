# Import socket module
import socket
import time


def make_text_valid(plain_text: str) -> str:
    plain_text_length = len(plain_text)
    extra_chars_count = 0 if plain_text_length % 3 == 0 \
        else 3 - (plain_text_length % 3)
    extra_chars = [chr(i) for i in range(123 - extra_chars_count, 123)]
    return plain_text + ''.join(extra_chars)


def make_key_valid(secret_key: str) -> str:
    if len(secret_key) == 9:
        return secret_key
    elif len(secret_key) > 9:
        return secret_key[:9]
    else:
        extra_chars = [chr(i) for i in range(123 - len(secret_key), 123)]
        return secret_key + ''.join(extra_chars)


def create_key_matrix(secret_key: str) -> list:
    matrix = []
    for i in range(3):
        matrix.append([])
        for j in range(3):
            count = (3 * i) + j
            matrix[-1].append(ord(secret_key[count]) - 97)

    return matrix


def matrix_multiplication(text_matrix: list, matrix: list) -> list:
    answer = []
    for i in range(3):
        val = 0
        for j in range(3):
            val += text_matrix[j] * matrix[j][i]
        answer.append(val % 26)

    return answer


def encrypt(plain_text: str, secret_key: str) -> str:
    plain_text = make_text_valid(plain_text)
    cipher_text = []
    secret_key = make_key_valid(secret_key)
    matrix = create_key_matrix(secret_key)
    for i in range(0, len(plain_text), 3):
        text_matrix = [ord(char) - 97 for char in plain_text[i : i + 3]]
        answer = matrix_multiplication(text_matrix, matrix)
        for char in answer:
            cipher_text.append(chr(char + 97))

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