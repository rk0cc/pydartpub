from enum import StrEnum
from furl import furl
from typing import Optional, Any

from ..client import PubRepositoryCursor
from .factory import PubApiClientFactory

class SearchOrder(StrEnum):
    TOP = "top"
    TEXT = "text"
    CREATED = "created"
    UPDATED = "updated"
    POPULARITY = "popularity"
    LIKE = "like"
    POINTS = "points"

class PubApiClientSearch(PubApiClientFactory):
    def __init__(self, cursor: PubRepositoryCursor):
        super().__init__(cursor)

    def _construct_url(self, kwargs: dict[str, Any]) -> str:
        page: int = kwargs["page"]
        query: Optional[str] = kwargs["query"]
        sort: Optional[SearchOrder] = kwargs["sort"]

        if page < 1:
            raise ValueError("Invalid page number")

        surl = furl(self._cursor.search_url)
        param = {}

        if query:
            param["q"] = query
        
        if page != 1:
            param["page"] = page

        if sort:
            param["sort"] = sort.lower()
        
        return surl.tostr()
    
    def execute(self, query: Optional[str] = None, page: int = 1, sort: Optional[SearchOrder] = None):
        return super().execute(**locals())
        
