import hashlib
import random
import string


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def generate_password() -> str:
    all_password_chars_list = list(string.ascii_letters + string.digits)
    random.shuffle(all_password_chars_list)
    return "".join(all_password_chars_list[0:8])

