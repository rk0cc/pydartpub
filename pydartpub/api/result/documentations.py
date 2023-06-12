from enum import Enum
from furl import furl
from typing import Optional, Sequence
from versions import Version

from ..client import PubRepositoryCursor
from ..url import get_repository_site

class DocumentStatus(Enum):
    PENDING = 0
    FAILED = 1
    SUCCESS = 2

class PubVersionDocumentation:
    def __init__(self, package_name: str, version: Version, status: DocumentStatus, has_documentation: bool):
        if has_documentation:
            assert status == DocumentStatus.SUCCESS

        self.__package_name = package_name
        self.__version = version
        self.__status = status
        self.__has_documentation = has_documentation

    @property
    def version(self) -> Version:
        return self.__version
    
    @property
    def status(self) -> DocumentStatus:
        return self.__status
    
    @property
    def has_documentation(self) -> bool:
        return self.__has_documentation

    def resolve_documentation_url(self) -> Optional[str]:
        if self.__has_documentation:
            return furl(get_repository_site()).add(path="documentation").add(path=self.__package_name).add(path=str(self.__version))
        
        return None

class PubDocumentation:
    def __init__(self, name: str, latest_stable_version: Version, versions: list[PubVersionDocumentation]):
        self.__name = name
        self.__latest_stable_version = latest_stable_version
        self.__versions = tuple(versions)

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def latest_stable_version(self) -> Version:
        return self.__latest_stable_version
    
    @property
    def versions(self) -> Sequence[PubVersionDocumentation]:
        return self.__versions
