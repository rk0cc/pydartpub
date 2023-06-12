import copy
from frozendict import frozendict
from typing import Optional, Any, Sequence
from versions import Version, VersionItem, parse_version, parse_version_set

from .dependency import PubDependency, DependencyDict, parse_dependencies_dict

class PubspecSerializable:
    """
    Define any subclass which related with pubspec and added convert to dict
    """
    def __iter__(self):
        for k in self.__dict__:
            yield k.lstrip("__"), getattr(self, k)

    def __str__(self):
        return str(dict(self))

class PubspecScreenshot(PubspecSerializable):
    """
    Get a screenshot information of corresponded pubspec
    """
    def __init__(self, description: str, path: str) -> None:
        """
        Create pubspec's screenshot information

        :param description: Description of this screenshot
        :param path: Related path of screenshot image in the project directory
        """
        self.__description = description
        self.__path = path

    @property
    def description(self) -> str:
        """
        Description of this screenshot
        """
        return self.__description
    
    @property
    def path(self) -> str:
        """
        Related path of screenshot image in the project directory
        """
        return self.__path

class Pubspec(PubspecSerializable):
    """
    Structure of `pubspec.yaml` in corresponded type in Python which replicate from
    `pubspec_parse` in Dart language - https://pub.dev/packages/pubspec_parse

    All properties in this object is read-only, and not designed for
    making modification under Python runtime.
    """

    def __init__(
            self,
            name: str,
            version: Optional[Version] = None,
            publish_to: Optional[str] = None,
            author: Optional[str] = None,
            authors: Optional[list[str]] = None,
            environment: Optional[dict[str, VersionItem]] = None,
            homepage: Optional[str] = None,
            repository: Optional[str] = None,
            issue_tracker: Optional[str] = None,
            funding: Optional[list[str]] = None,
            topics: Optional[list[str]] = None,
            screenshots: Optional[list[PubspecScreenshot]] = None,
            documentation: Optional[str] = None,
            description: Optional[str] = None,
            dependencies: Optional[DependencyDict] = None,
            dev_dependencies: Optional[DependencyDict] = None,
            dependency_overrides: Optional[DependencyDict] = None,
            flutter: Optional[dict[str, Any]] = None
        ) -> None:
        """
        Construct a pubspec in given objects.

        All parameters are optional except `name`

        :param name: Name of the project (mandatory).
        :param version: Version of given project (optional, but required for publish)
        :param publish_to: Either specify an URL of external repository host or `none` for package which won't publish publicly
        :param author: Name of developer, it deprecated since Dart 2.7
        :param authors: Same as `author` with multiple developers and also deprecated since Dart 2.7
        :param environment: Version constraint of Dart's environment
        :param homepage: Homepage of this project
        :param repository: Source code hosting site of this project
        :param issue_tracker: Issues trascking page of this project
        :param funding: URL link(s) of sponsorship
        :param topics: Define topics (or hashtags) for this project
        :param screenshots: Screenshot of package implementation
        :param documentation: Documentation page of this project
        :param description: Description of this package
        :param dependencies: Another projects uses in this project and will be downloaded when referencing
        :param dev_dependencies: Same as `dev_dependencies`, but will not implement in referenced project
        :param dependency_overrides: Override the project's information rather than `dependencies`
        :param flutter: Additional configurations for Flutter projects
        """
        self.__name = name
        self.__version = version
        self.__publish_to = publish_to
        self.__author = author
        self.__authors = tuple(authors) if authors else None
        self.__environment = frozendict(environment) if environment else None
        self.__homepage = homepage
        self.__repository = repository
        self.__issue_tracker = issue_tracker
        self.__funding = tuple(funding) if funding else None
        self.__topics = tuple(topics) if topics else None
        self.__screenshots = tuple(screenshots) if screenshots else None
        self.__documentation = documentation
        self.__description = description
        self.__dependencies = frozendict(dependencies) if dependencies else None
        self.__dev_dependencies = frozendict(dev_dependencies) if dev_dependencies else None
        self.__dependency_overrides = frozendict(dependency_overrides) if dependency_overrides else None
        self.__flutter = frozendict(flutter) if flutter else None

    @property    
    def name(self) -> str:
        """
        Name of the project
        """
        return self.__name
    
    @property
    def version(self) -> Optional[Version]:
        """
        Version of given project
        """
        return self.__version
    
    @property
    def publish_to(self) -> Optional[str]:
        """
        Either specify an URL of external repository host or `none` for package which won't publish publicly
        """
        return self.__publish_to
    
    @property
    def author(self) -> Optional[str]:
        """
        Name of developer, it deprecated since Dart 2.7
        """
        return self.__author
    
    @property
    def authors(self) -> Optional[Sequence[str]]:
        """
        Same as `author` with multiple developers and also deprecated since Dart 2.7
        """
        return self.__authors
    
    @property
    def environment(self) -> Optional[dict[str, VersionItem]]:
        """
        Version constraint of Dart's environment
        """
        return self.__environment
    
    @property
    def homepage(self) -> Optional[str]:
        """
        Homepage of this project
        """
        return self.__homepage
    
    @property
    def repository(self) -> Optional[str]:
        """
        Source code hosting site of this project
        """
        return self.__repository
    
    @property
    def issue_tracker(self) -> Optional[str]:
        """
        Issues trascking page of this project
        """
        return self.__issue_tracker
    
    @property
    def funding(self) -> Optional[Sequence[str]]:
        """
        URL link(s) of sponsorship
        """
        return self.__funding
    
    @property
    def topics(self) -> Optional[Sequence[str]]:
        """
        Define topics (or hashtags) for this project
        """
        return self.__topics
    
    @property
    def screenshots(self) -> Optional[Sequence[PubspecScreenshot]]:
        """
        Screenshot of package implementation
        """
        return self.__screenshots
    
    @property
    def documentation(self) -> Optional[str]:
        """
        Documentation page of this project
        """
        return self.__documentation
    
    @property
    def description(self) -> Optional[str]:
        """
        Description of this package
        """
        return self.__description
    
    @property
    def dependencies(self) -> Optional[DependencyDict]:
        """
        Another projects uses in this project and will be downloaded when referencing
        """
        return self.__dependencies
    
    @property
    def dev_dependencies(self) -> Optional[DependencyDict]:
        """
        Same as `dev_dependencies`, but will not implement in referenced project
        """
        return self.__dev_dependencies
    
    @property
    def dependency_overrides(self) -> Optional[DependencyDict]:
        """
        Override the project's information rather than `dependencies`
        """
        return self.__dependency_overrides
    
    @property
    def flutter(self) -> Optional[dict[str, Any]]:
        """
        Additional configurations for Flutter projects
        """
        return self.__flutter
    

def parse_from_dict(json: dict) -> Pubspec:
    """
    Apply pubspec dictionary to `Pubspec` object via applying as `**kwargs`

    :param json: Pubspec's JSON

    :return: Pubsepc object
    """
    json_data = {
        k: v for k, v in copy.deepcopy(json)  # Prevent any containers can be modified during parse
        if k in {pk.lstrip("__") for pk in Pubspec.__dict__.keys()}
    }
    pending_update = {}  # Pending convert to Python's objects
    
    ver_str = json_data.get("version")
    if ver_str:
        pending_update["version"] = parse_version(ver_str)

    env_rawmap = json_data.get("environment")
    if env_rawmap:
        pending_update["environment"] = {k: parse_version_set(v) for k, v in dict(env_rawmap).items()}

    sc_raw = json_data.get("screenshot")
    if sc_raw:
        pending_update["screenshot"] = [PubspecScreenshot(i["description"], i["path"]) for i in sc_raw]

    for deps_keys in "dependencies", "dev_dependencies", "dependency_overrides":
        deps_raw = json_data.get(deps_keys)
        if deps_raw:
            pending_update[deps_keys] = {k: parse_dependencies_dict(v) for k, v in dict(deps_raw).items()}

    json_data.update(pending_update)

    return Pubspec(**json_data)
    
