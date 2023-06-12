import os
import urllib.parse


def get_repository_site(default_url: str = "https://pub.dev/") -> str:
    '''
    Get an API URL of pub repository server.
    
    :param default_url: Default URL of pub repository server if `PUB_HOSTED_URL` is undefined in environment
    '''
    base_url = os.environ.get("PUB_HOSTED_URL", default_url)
    return urllib.parse.urljoin(base_url, "api/")
