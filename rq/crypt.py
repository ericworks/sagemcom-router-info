import hashlib
import random

from passlib.handlers.sha2_crypt import sha512_crypt


def sha512crypt(a, b):
    # Split the salt
    e = b.split('$')
    c = None
    d = '$6$'
    if len(e) > 1:
        if e[1] != '6':
            raise ValueError(f"Got '{b}' but only SHA512 ($6$) algorithm supported")
        c = int(e[2].split('=')[1])
        if c:
            c = min(max(c, 1000), 999999999)
            b = e[3] if len(e) > 3 else b
        else:
            b = e[2] if len(e) > 2 else b
    if len(b) < 8 or len(b) > 16:
        raise ValueError(f"Wrong salt length: '{len(b)}' bytes when 8 <= n <= 16 expected. Got salt '{b}'.")

    # Hash the password with the provided salt
    hashed_password = sha512_crypt.using(salt=b, rounds=c or 5000).hash(a)

    return hashed_password


def _sha512_wrapper(a: str) -> str:
    return hashlib.sha512(a.encode("UTF-8")).hexdigest()



def _generate_cnonce() -> str:
    random_number = random.random() * 10000000000000000000
    return str(int(random_number)).ljust(19, "0")


def _generate_auth_key(user: str, raw_password: str, nonce: str, salt: str, cnonce: str) -> str:
    g_content = user + ":" + nonce + ":" + sha512crypt(raw_password, salt)[3:]
    g = _sha512_wrapper(g_content)
    return _sha512_wrapper(g + ":0:" + cnonce)


def get_login_auth_data(user: str, password: str, nonce: str, salt: str) -> dict:

    cnonce = _generate_cnonce()
    login_data = {
        "login": user,
        "auth_key": _generate_auth_key(user, password, nonce, salt, cnonce),
        "cnonce": cnonce
    }
    return login_data





if __name__ == "__main__":

    print(_generate_cnonce())


    print(sha512crypt("ADMIN", "GBZqaHom2a/"))

    salt = "GBZq6Hom2d/"
    nonce = "810061089"

    cnonce = _generate_cnonce()
    cnonce = "0907380530864216800"

    user = "admin"
    password = "ADMIN"

    print(_generate_auth_key(user, password, nonce, salt, cnonce))

