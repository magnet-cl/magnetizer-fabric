from fabric.api import hide, run, settings


def install(package, upgrade=False):
    """
    Helper method to install a deb package.

    If the package is already installed and the parameter 'upgrade' is True,
    then it will be upgraded if possible.

    """
    cmd = ''
    if not is_installed(package):
    	cmd = 'brew install {}'.format(package)
    elif upgrade:
    	cmd = 'brew reinstall {}'.format(package)

    if cmd:
        run(cmd)


def update_index():
    cmd = 'brew update'
    run(cmd)


def is_installed(pkg_name):
    with settings(
	hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
	res = run("brew ls --versions %(pkg_name)s" % locals())
	for line in res.splitlines():
	    return True
	return False
