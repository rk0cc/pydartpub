from furl import furl
import os


def get_repository_site(default_url: str = "https://pub.dev/") -> furl:
    '''
    Get an entrypoint of API URL of pub repository server.
    
    :param default_url: Default URL of pub repository server if `PUB_HOSTED_URL` is undefined in environment
    '''
    return furl(os.environ.get("PUB_HOSTED_URL", default_url))
   