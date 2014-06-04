from fabric.api import cd
from fabric.api import run
from fabric.api import sudo
from fabric.api import task
from fabric.colors import green
from fabtools import deb
from fabtools import service

from fabfile import utils


@task
def install():
    """ Installs redis """

    # update apt index
    deb.update_index(quiet=False)

    # requirements
    utils.deb.install('build-essential')

    print(green('Downloading redis 2.8.9'))
    run('wget http://download.redis.io/releases/redis-2.8.9.tar.gz')

    print(green('Building redis'))
    run('tar xzf redis-2.8.9.tar.gz')
    with cd('redis-2.8.9'):
        run('make')

    print(green('Installing redis'))
    with cd('redis-2.8.9'):
        sudo('make install')

    print(green('Setting redis to run as daemon'))
    with cd('redis-2.8.9/utils'):
        sudo('./install_server.sh')

    print(green('Setting redis to start automatically at boot, '
                'assuming default settings'))
    sudo('update-rc.d redis_6379 defaults')


@task
def start():
    """ Starts redis daemon """
    service.start('redis_6379')


@task
def stop():
    """ Starts redis daemon """
    service.stop('redis_6379')
