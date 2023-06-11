from pypub.url import get_repository_site

class PubRepositoryClient:
    def __init__(self) -> None:
        self._repository = get_repository_site()