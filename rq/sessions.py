from __future__ import annotations

import os
import pickle

import requests
from requests import Session


class RequestSessionMgr:
    _instance = None

    def __init__(self):
        if RequestSessionMgr._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RequestSessionMgr._instance = self

        # if pickle file exists then load session from file
        try:
            if os.path.exists("session.pkl"):
                with open("session.pkl", "rb") as f:
                    self.sessions = pickle.load(f)

            else:

                self.sessions = requests.Session()
        except Exception as e:
            print(e)
            self.sessions = requests.Session()

    def save_session_to_file(self):
        with open("session.pkl", "wb") as f:
            pickle.dump(self.sessions, f)

    @staticmethod
    def get_session() -> Session:
        return RequestSessionMgr.get_instance().m_get_session()

    @staticmethod
    def get_instance() -> RequestSessionMgr:
        if RequestSessionMgr._instance is None:
            RequestSessionMgr()
        return RequestSessionMgr._instance

    def m_get_session(self) -> Session:
        return self.sessions
