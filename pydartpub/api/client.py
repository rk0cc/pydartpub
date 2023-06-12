from .url import get_repository_site


class PubRepositoryCursor:
    def __init__(self) -> None:
        self.__repository = get_repository_site() / "api"

    @property
    def search_url(self) -> str:
        return (self.__repository / "search").tostr()
    
    @property
    def packages_url(self) -> str:
        return (self.__repository / "package").tostr()
    
    @property
    def documentation_url(self) -> str:
        return (self.__repository / "documentation").tostr()
    
