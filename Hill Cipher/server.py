import socket


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


def modInverse(a, m):
    for x in range(1, m):
        if ((a % m) * (x % m)) % m == 1:
            return x

    return -1


def matrix_multiplication(text_matrix: list, matrix: list) -> list:
    answer = []
    for i in range(3):
        val = 0
        for j in range(3):
            val += text_matrix[j] * matrix[j][i]
        answer.append(val % 26)

    return answer


def transpose_matrix(m):
    return list(map(list, zip(*m)))


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def get_matrix_determinant(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))
    return determinant


def get_matrix_inverse(m):
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = get_matrix_minor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * get_matrix_determinant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose_matrix(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] % 26
    return cofactors


def decrypt(cipher_text: str, secret_key: str) -> str:
    plain_text = []
    secret_key = make_key_valid(secret_key)
    matrix = create_key_matrix(secret_key)
    determinant = get_matrix_determinant(matrix)
    mod = determinant % 26
    mod_inverse = modInverse(mod, 26)
    inverse = get_matrix_inverse(matrix)
    for i in range(3):
        for j in range(3):
            inverse[i][j] = (mod_inverse * inverse[i][j]) % 26

    for i in range(0, len(cipher_text), 3):
        text_matrix = [ord(char) - 97 for char in cipher_text[i: i + 3]]
        answer = matrix_multiplication(text_matrix, inverse)
        for char in answer:
            plain_text.append(chr(int(char + 97)))

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

# rrfvsvcct