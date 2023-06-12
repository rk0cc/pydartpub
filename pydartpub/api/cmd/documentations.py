from furl import furl
from typing import Any

from ..client import PubRepositoryCursor
from .factory import PubApiClientFactory

class PubApiClientDocumentation(PubApiClientFactory):
    def __init__(self, cursor: PubRepositoryCursor):
        super().__init__(cursor)

    def _construct_url(self, kwargs: dict[str, Any]) -> str:
        return (furl(self._cursor.documentation_url) / kwargs["package_name"]).tostr()
    
    def execute(self, package_name: str):
        return super().execute(**locals())
