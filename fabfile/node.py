from fabric.api import task, run
from fabric.colors import green
from fabtools import deb

from fabfile import utils


@task
def install():
    """ Installs node """
    # update apt index
    deb.update_index(quiet=False)

    # install node, taken form
    # http://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
    print(green('Installing dependencies'))
    utils.deb.install('python-software-properties')
    utils.deb.install('python')
    utils.deb.install('g++')
    utils.deb.install('make')

    print(green('Adding ppa:chris-lea/node.js to apt repositories'))
    run('sudo add-apt-repository ppa:chris-lea/node.js')
    deb.update_index(quiet=False)

    print(green('Installing nodejs'))
    utils.deb.install('nodejs')
