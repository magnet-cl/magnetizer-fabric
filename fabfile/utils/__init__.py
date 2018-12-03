from distutils.util import strtobool
from fabfile.utils import os_commands


def arg_to_bool(arg):
    """ Converts a given task argument into a bool

    The goal of this method is to convert a fabric argument intended as a bool
    representation into a Python bool.

    In case that the argument is not a supported string representation (for
    strtobool) of a bool it will raise an exception.

    If the argument is not a string it will return a cast of the argument into
    a bool.

    """

    if isinstance(arg, str):
        return bool(strtobool(arg))
    else:
        return bool(arg)
