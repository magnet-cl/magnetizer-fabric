from fabric.api import cd
from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
from fabric.contrib.files import exists
from fabric.contrib.files import sed

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
    plugins = ['exuberant-ctags', 'ack-grep', 'pyflakes', 'clang']
    for plugin in plugins:
        utils.os_commands.install(plugin)

    # install pip if is not available
    utils.os_commands.install('python-pip')

    # update pip through pip
    py_install('pip', use_sudo=True, upgrade=True)

    # TODO Check if the command python get-pip.py is better
    # install and upgrade setup tools (that replaced distribute)
    py_install('setuptools', use_sudo=True, upgrade=True)

    # python flake+pep8
    if not py_is_installed('flake8'):
        py_install('flake8', use_sudo=True)

    # js linter
    if utils.os_commands.is_installed('nodejs'):
        cmd = 'sudo -H npm -g install jscs'
        run(cmd)
    else:
        print(red('npm not installed. Re-run this task after installing npm'))


@task
def install():
    """ Installs and configures vim """
    # update apt index
    utils.os_commands.update_index(quiet=False)

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
    # plugins dependencies
    install_dependencies()

    # git pull
    with cd('.vim'):
        print(green('Updating .vim folder'))
        git_pull()

        print(green('Updating submodules'))
        run('git submodule update --init')

    # plugins update
    cmd = 'vim +NeoBundleUpdate +qa!'
    run(cmd)


@task
def set_js_linter():
    """ Sets the standard JS linter on syntastic """

    # patterns
    before = '^let g:syntastic_javascript_checkers.*$'
    after = 'let g:syntastic_javascript_checkers = ["jscs"]'

    print(green('Setting jscs as the default linter on vim.'))
    sed('.vim/vimrc', before, after)

    print(green('Uploading configuration file'))
    config_path = 'conventions/.jscsrc'
    put(config_path)
