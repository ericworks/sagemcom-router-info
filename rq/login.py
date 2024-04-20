from requests import Session
from rq.common import common_headers, login_param_url, login_url
from rq.crypt import get_login_auth_data
from rq.sessions import RequestSessionMgr


class LoginParamException(Exception):
    pass


class LoginFailedException(Exception):
    pass


def _get_session() -> Session:
    return RequestSessionMgr.get_session()


def _get_login_param(user: str) -> dict:
    login_param_data = {
        "login": user
    }
    login_params = _get_session().post(login_param_url, data=login_param_data, headers=common_headers)
    nonce = login_params.cookies.get("nonce", None)
    salt = login_params.cookies.get("salt", None)
    if nonce is None or salt is None:
        raise LoginParamException("Nonce or Salt is Empty.")
    return {"nonce": nonce, "salt": salt}


def _do_login(user: str, password: str, login_param: dict) -> None:
    login_data = get_login_auth_data(user, password, login_param["nonce"], login_param["salt"])
    t = _get_session().post(login_url, data=login_data, headers=common_headers)
    if t.status_code < 200 or t.status_code >= 400:
        raise LoginFailedException(f"Login failed with status code {t.status_code}")


def do_login(user: str, raw_password: str):
    login_param = _get_login_param(user)
    _do_login(user, raw_password, login_param)


if __name__ == "__main__":
    do_login("admin", "password")
