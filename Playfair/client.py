# Import socket module
import socket
import time

def create_matrix(secret_key):
    matrix = [[] for _ in range(5)]
    chars = [chr(i) for i in range(97, 123)]
    curr_row = 0
    for char in secret_key:
        # print(char)
        if len(matrix[curr_row]) == 5:
            curr_row += 1
        if char in chars:
            if char == 'i':
                matrix[curr_row].append(char + 'j')
                chars.remove('j')
            else:
                matrix[curr_row].append(char)

            chars.remove(char)
        else:
            continue

    for char in chars:
        if char == 'j':
            continue
        if len(matrix[curr_row]) == 5:
            curr_row += 1
        if char == 'i':
            matrix[curr_row].append('ij')
        else:
            matrix[curr_row].append(char)
        # print(matrix, curr_row)
    return matrix

def split_and_pad(plain_text):
    splits = []
    i = 0
    while i < len(plain_text) - 1:
        if plain_text[i] != plain_text[i + 1]:
            splits.append(plain_text[i] + plain_text[i + 1])
            i += 2
        else:
            splits.append(plain_text[i] + 'x')
            i += 1

    return splits

def find_row_col(matrix, char):
    for i in range(5):
        for j in range(5):
            if char == 'i' or char == 'j':
                if matrix[i][j] == 'ij':
                    return i, j
            else:
                if matrix[i][j] == char:
                    return i, j


def encrypt(plain_text, secret_key):
    matrix = create_matrix(secret_key)
    splits = split_and_pad(plain_text)
    cipher_text = []
    for split in splits:
        r1, c1 = find_row_col(matrix, split[0])
        r2, c2 = find_row_col(matrix, split[1])
        first_char, second_char = '', ''
        if r1 == r2:
            first_char = matrix[r1][(c1 + 1) % 5]
            second_char = matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            first_char = matrix[(r1 + 1) % 5][c1]
            second_char = matrix[(r2 + 1) % 5][c2]
        else:
            first_char = matrix[r1][c2]
            second_char = matrix[r2][c1]

        if first_char == 'ij':
            first_char = 'i'
        elif second_char == 'ij':
            second_char = 'i'
        cipher_text.append(first_char + second_char)

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

# print(encrypt(plain_text, secret_key))

s.send(encrypt(plain_text, secret_key).encode())
time.sleep(0.5)
s.send(secret_key.encode())
print("Message sent")
s.close()
