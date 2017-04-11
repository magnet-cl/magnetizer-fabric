import platform
from fabric.api import run

from fabfile.utils import deb


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)


def git_pull():
    """ Git pull. """
    cmd = 'git pull'
    run(cmd)


def git_install():
    """ Utility method that installs git if is not available. """
    if platform.system().lower() == 'linux':
        deb.install('git')
