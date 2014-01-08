from fabric.api import task, run, cd
from fabric.colors import green, red
from fabric.contrib.files import exists

from fabtools.deb import update_index
from fabtools.python import install as py_install
from fabtools.python import is_installed as py_is_installed

from fabfile.git import git_clone, git_install, git_pull
from fabfile import utils


@task
def install_dependencies():
    # install vim
    utils.deb.install('vim')

    # install required packages by plugins
    print(green('Installing plugins dependencies.'))
    # ctags, better grep, python flake, C/C++ omnicompletion
    plugins = ['exuberant-ctags', 'ack-grep', 'pyflakes', 'clang',
               'rhino']
    for plugin in plugins:
        utils.deb.install(plugin)

    # install pip if is not available
    utils.deb.install('python-pip')
    if not py_is_installed('flake8'):
        py_install('flake8', use_sudo=True)  # python flake+pep8


@task
def install():
    """ Installs and configures vim """
    # update apt index
    update_index(quiet=False)

    install_dependencies()

    # backup vim configuration folder
    if exists('.vim'):
        print(green('Backing up your vim configuration folder to .vim-bkp'))
        cmd = 'mv .vim .vim-bkp'
        run(cmd)

    # backup vim configuration file
    if exists('.vimrc'):
        print(green('Backing up your vim configuration file to .vimrc-bkp'))
        cmd = 'mv .vimrc .vimrc-bkp'
        run(cmd)

    # clone vim_config repository
    print(green('Cloning Vim_config repository.'))
    # install git if is not available
    git_install()
    git_clone('git://github.com/magnet-cl/Vim_config.git', '.vim')

    # installation script
    print(green('Installing Vim_config.'))
    with cd('.vim'):
        cmd = 'source install.sh'
        run(cmd)


@task
def restore_backup():
    """ Restores backup vim configuration. """

    # restore vim configuration folder
    if exists('.vim-bkp'):
        print(green('Restoring your vim configuration folder.'))
        cmd = 'rm -rf .vim'
        run(cmd)
        cmd = 'mv .vim-bkp .vim'
        run(cmd)
    else:
        print(red('vim-bkp folder not found.'))

    # restore vim configuration file
    if exists('.vimrc-bkp'):
        print(green('Restoring your vim configuration file.'))
        cmd = 'rm -rf .vimrc'
        run(cmd)
        cmd = 'mv .vimrc-bkp .vimrc'
        run(cmd)
    else:
        print(red('vimrc-bkp file not found.'))


@task
def update():
    """ Updates vim repository and plugins. """
    # git pull
    with cd('.vim'):
        git_pull()

    # plugins update
    cmd = 'vim +NeoBundleUpdate +qa!'
    run(cmd)
