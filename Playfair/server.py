import socket

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

def split_and_pad(cipher_text):
    splits = []
    i = 0
    while i < len(cipher_text) - 1:
        splits.append(cipher_text[i : i + 2])
        i += 2

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

def decrypt(cipher_text: str, secret_key: str) -> str:
    plain_text = []
    matrix = create_matrix(secret_key)
    splits = split_and_pad(cipher_text)
    for split in splits:
        r1, c1 = find_row_col(matrix, split[0])
        r2, c2 = find_row_col(matrix, split[1])
        first_char, second_char = '', ''
        if r1 == r2:
            first_char = matrix[r1][(c1 - 1) % 5]
            second_char = matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            first_char = matrix[(r1 - 1) % 5][c1]
            second_char = matrix[(r2 - 1) % 5][c2]
        else:
            first_char = matrix[r1][c2]
            second_char = matrix[r2][c1]

        if first_char == 'ij':
            first_char = 'i'
        elif second_char == 'ij':
            second_char = 'i'
        plain_text.append(first_char + second_char)

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
    # print(split_and_pad(cipher_text))