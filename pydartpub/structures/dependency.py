import abc
from frozendict import frozendict
from typing import Optional, Any, Union
from versions import VersionItem, parse_version_set

VersionConstraint = Optional[VersionItem]
RawDependencyDictValue = Union[str, dict[str, Any]]
RawDependencyDict = dict[str, Optional[RawDependencyDictValue]]

def __version_constraint_in_str(version: VersionConstraint) -> str:
    return str(version) if version else "any"

class PubDependency(abc.ABC):
    @abc.abstractmethod
    def generate_dict_value(self) -> RawDependencyDictValue:
        raise NotImplementedError()
    
    def __str__(self) -> str:
        return str(self.generate_dict_value())
    
DependencyDict = dict[str, PubDependency]

class PubHostedDependency(PubDependency):
    def __init__(self, version: VersionConstraint):
        self.__version = version

    @property
    def version(self) -> VersionConstraint:
        return self.__version

    def generate_dict_value(self) -> RawDependencyDictValue:
        return __version_constraint_in_str(self.__version)

class PubExternalHostedDependency(PubHostedDependency):
    def __init__(self, version: VersionConstraint, hosted: str, name: Optional[str] = None):
        super().__init__(version)
        self.__hosted = hosted
        self.__name = name

    @property
    def hosted(self) -> str:
        return self.__hosted
    
    @property
    def name(self) -> Optional[str]:
        return self.__name

    def generate_dict_value(self) -> RawDependencyDictValue:
        return frozendict({
            "hosted": self.__hosted if not self.__name else {
                "name": self.__name,
                "url": self.__hosted
            },
            "version": super().generate_dict_value()
        })
    
class PubGitDependency(PubDependency):
    def __init__(self, url: str, path: Optional[str], ref: Optional[str]):
        self.__url = url
        self.__path = path
        self.__ref = ref

    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def path(self) -> Optional[str]:
        return self.__path
    
    @property
    def ref(self) -> Optional[str]:
        return self.__ref
    
    def generate_dict_value(self) -> RawDependencyDictValue:
        git_context = None
        context = {
            "git": git_context
        }
        
        if not self.__path and not self.__ref:
            git_context = self.__url
        else:
            git_context = {
                "url": self.__url
            }
            for (k, v) in ("path", self.__path), ("ref", self.__ref):
                if v:
                    git_context[k] = v

        return frozendict(context)

class PubPathDependency(PubDependency):
    def __init__(self, path: str):
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path
    
    def generate_dict_value(self) -> RawDependencyDictValue:
        return frozendict({"path": self.__path})

class PubSdkDependency(PubDependency):
    def __init__(self, sdk: str, version: VersionConstraint):
        self.__sdk = sdk
        self.__version = version

    @property
    def sdk(self) -> str:
        return self.__sdk
    
    @property
    def version(self) -> VersionConstraint:
        return self.__version
    
    def generate_dict_value(self) -> RawDependencyDictValue:
        context = {"sdk": self.__sdk}
        if self.__version:
            context["version"] = str(self.__version)
        
        return frozendict(context)


def parse_dependencies_dict(dependencies_dict: RawDependencyDict) -> DependencyDict:
    def dependency_parser(rdv: Optional[RawDependencyDictValue]):
        match rdv:
            case None:
                return PubHostedDependency()
            case str() as rdv:
                return PubHostedDependency(parse_version_set(rdv))
            case dict() as rdv:
                xtra_dep_key = rdv.keys()[0]
                xtra_dep = rdv.get(xtra_dep_key)
                match xtra_dep_key:
                    case "hosted":
                        ver = rdv.get("version")
                        ver = parse_version_set(ver) if ver else None
                        if isinstance(xtra_dep, str):
                            return PubExternalHostedDependency(ver, xtra_dep)
                        else:
                            return PubExternalHostedDependency(ver, xtra_dep["url"], str(xtra_dep["name"]))
                    case "git":
                        if isinstance(xtra_dep, str):
                            return PubGitDependency(xtra_dep)
                        else:
                            return PubGitDependency(xtra_dep["url"], xtra_dep.get("path"), xtra_dep.get("ref"))
                    case "path":
                        return PubPathDependency(xtra_dep)
                    case "sdk":
                        return PubSdkDependency(xtra_dep, rdv.get("version"))
                    case _:
                        raise KeyError("Unknown keys in dependencies map - " + xtra_dep_key)
            case _:
                raise TypeError()
            
    return frozendict({k: dependency_parser(v) for k, v in dependencies_dict})
