# fabric
from fabric.api import env
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabric.contrib.files import append

# fabtools
from fabtools import deb
from fabtools import user

from fabfile import utils


@task
def install():
    # add pgp key
    print(green('Adding PGP key'))
    deb.add_apt_key(keyid='58118E89F3A912897C070ADBF76221572C52609D',
                    keyserver='p80.pool.sks-keyservers.net')

    # add https support for apt
    utils.deb.install('apt-transport-https')

    # obtain the LSB version name
    id_, release, codename = run('lsb_release --id --release --codename --short').split("\r\n")

    # add docker apt sources list
    source = "deb https://apt.dockerproject.org/repo {}-{} main".format(id_.lower(), codename)
    append('/etc/apt/sources.list.d/docker.list', source, use_sudo=True)
    
    # update apt index
    deb.update_index(quiet=False)

    # install docker.io
    utils.deb.install('docker-engine')

    # add current user to docker group
    current_user = env.user
    cmd = "gpasswd -a {} docker".format(current_user)
    sudo(cmd)
