from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import exists
from fabtools.deb import update_index

from os.path import abspath
from os.path import dirname

import utils

ROOT_FOLDER = dirname(abspath(__file__))


@task
def install():
    """ Installs tmux. """
    # update apt index
    update_index(quiet=False)

    # install terminal definitions
    utils._deb.install('ncurses-term')

    # install tmux
    utils._deb.install('tmux')

    # upload configuration file
    configure()

    # upload tmux.sh
    destination_folder = '~/bin'
    if not exists(destination_folder):
        cmd = 'mkdir {}'.format(destination_folder)
        run(cmd)
    tmux_script = '{}/templates/tmux.sh'.format(ROOT_FOLDER)
    put(tmux_script, destination_folder, mode=0775)


@task
def configure():
    """ Uploads configuration file for tmux. """

    configuration_file = '{}/templates/tmux.conf'.format(ROOT_FOLDER)
    destination_file = '.tmux.conf'

    print(green('Uploading configuration file...'))
    put(configuration_file, destination_file)
