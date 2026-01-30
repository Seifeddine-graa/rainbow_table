import hashlib
import random
import math

# Jeu de caractère utilisé
charset = "abcdefghijklmnopqrstuvwxyz123456"
# Taille des mots de passes
password_length = 5


def generate_password() -> str:
    return "".join(random.choices(charset, k=password_length))


def md5_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def reduce(hash: str, level: int) -> str:
    bits = 5 * password_length
    hex_characters = math.ceil(bits / 4)
    reduction_hash = md5_hash(f"{hash}{level}")[:hex_characters]
    value = int(reduction_hash, 16)

    password = ""
    for _ in range(password_length):
        password += charset[value % len(charset)]
        value //= len(charset)

    return password


class Passwords:
    def __init__(self, length: int = password_length):
        self.length = length
        self.current = [0] * length

    def __iter__(self):
        return self

    def __len__(self):
        return len(charset) ** self.length

    def __next__(self):
        for i in range(self.length):
            if self.current[i] < len(charset) - 1:
                self.current[i] += 1
                return "".join(charset[c] for c in self.current)
            else:
                self.current[i] = 0
        raise StopIteration


def all_passwords(length: int = password_length):
    return Passwords(length)
