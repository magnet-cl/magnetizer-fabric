from fabric.api import task, run
from fabric.colors import green
from fabtools import deb

import utils


@task
def install():
    """ Installs node """
    print(green('Adding ppa:chris-lea/node.js to apt repositories'))
    run('sudo add-apt-repository ppa:chris-lea/node.js')

    # update apt index
    deb.update_index(quiet=False)

    # install node, taken form
    # http://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
    print(green('Installing dependencies'))
    utils._deb.install('python-software-properties')
    utils._deb.install('python')
    utils._deb.install('g++')
    utils._deb.install('make')

    print(green('Installing nodejs'))
    utils._deb.install('nodejs')
