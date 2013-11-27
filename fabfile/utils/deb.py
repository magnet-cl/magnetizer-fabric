from fabtools.deb import is_installed, install as deb_install


def install(package):
    """ Helper method to install a deb package if is not already installed. """
    if not is_installed(package):
        deb_install(package)
