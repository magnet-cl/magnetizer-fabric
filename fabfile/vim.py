from fabric.api import task, run, sudo
from fabric.colors import green, red
from fabric.contrib.files import exists

from deb_handler import apt_install
from git import git_clone


@task
def install():
    """ Installs and configures vim """
    # install vim
    apt_install('vim')

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
    git_clone('git://github.com/jslopez/Vim_config.git', '.vim')

    # install required packages by plugins
    print(green('Installing plugins dependencies.'))
    apt_install('exuberant-ctags')  # ctags
    apt_install('ack-grep')  # better grep
    apt_install('pyflakes')  # python flake
    sudo('pip install flake8')  # python flake+pep8
    apt_install('lacheck')  # latex
    apt_install('clang')  # C/C++ omnicompletion

    # installation script
    print(green('Installing Vim_config.'))
    cmd = 'source .vim/install.sh'
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
