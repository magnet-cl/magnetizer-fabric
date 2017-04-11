import platform
from fabfile.utils import darwin
from fabfile.utils import deb


def get_handler():
    if platform.system().lower() == 'darwin':
        return darwin
    else:
        # assume debian
        return deb


def install(*args, **kwargs):
    handler = get_handler()
    handler.install(*args, **kwargs)


def update_index(*args, **kwargs):
    handler = get_handler()
    handler.update_index(*args, **kwargs)


def is_installed(*args, **kwargs):
    handler = get_handler()
    handler.is_installed(*args, **kwargs)
