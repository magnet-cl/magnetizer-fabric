from fabric.api import run


def install(package, upgrade=False):
    """
    Helper method to install a deb package.

    If the package is already installed and the parameter 'upgrade' is True,
    then it will be upgraded if possible.

    """
    cmd = 'brew install {}'.format(package)
    run(cmd)


def update_index():
    cmd = 'brew update'
    run(cmd)
