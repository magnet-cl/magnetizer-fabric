from fabric.api import sudo


def apt_update():
    """ Helper method to resynchronize the package index files from their
    sources. """
    cmd = 'apt-get update'
    sudo(cmd)


def apt_install(package):
    """ Helper method to install deb packages through apt-get. """
    cmd = 'apt-get install -y %s' % package
    sudo(cmd)
