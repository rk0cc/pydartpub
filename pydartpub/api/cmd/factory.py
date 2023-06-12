import abc
import copy
import json
import platform
import requests as req
import sys
from typing import Any, Iterable

from ... import PYDARTPUB_VERSION
from ..client import PubRepositoryCursor

class ResponseError(ConnectionError):
    def __init__(self, response_code: int):
        super().__init__("The response returned with error code: {}".format(response_code))
        self.__response_code = response_code

    @property
    def response_code(self):
        return self.__response_code

class PubApiClientFactory(abc.ABC):
    def __init__(self, cursor: PubRepositoryCursor):
        self._cursor = cursor

    @property
    @staticmethod
    def user_agent() -> str:
        python_ver = "{0}.{1}.{2}".format(*sys.version_info[:3])
        pun = platform.uname()
        return "pydartpub {} (Python {}; {} {}; {})".format(PYDARTPUB_VERSION, python_ver, pun.system, pun.version, pun.machine)


    @abc.abstractmethod
    def _construct_url(self, kwargs: dict[str, Any]) -> str:
        raise NotImplementedError()

    def __do_request(self, kwargs: dict[str, Any]) -> Any:
        parsed_local_var = copy.copy(kwargs)
        if "self" in parsed_local_var:
            del parsed_local_var["self"]

        resp = req.get(
            url=self._construct_url(parsed_local_var),
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
                "Accept-Encoding": "gzip"
            },
            allow_redirects=True
        )

        if resp.status_code != 200:
            raise ResponseError(resp.status_code)
        
        return resp.json()
    
    def execute(self, **kwargs):
        return self.__do_request(kwargs)
