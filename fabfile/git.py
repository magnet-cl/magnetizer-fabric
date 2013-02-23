from fabric.api import run

from utils import _deb


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
    _deb.install('git')
