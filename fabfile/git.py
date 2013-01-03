from fabric.api import run


def git_clone(url, path):
    """ Utility method to clone git repositories. """
    cmd = 'git clone %s %s' % (url, path)
    run(cmd)
