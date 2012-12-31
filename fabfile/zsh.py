from fabric.api import task, run, env, put
from fabric.colors import green

from deb_handler import apt_install


@task
def install():
    """ Installs and sets zsh as default shell """
    # install zsh
    apt_install('zsh')

    # install zsh examples
    apt_install('zsh-lovers')

    # set as default shell for the user
    cmd = 'chsh -s /bin/zsh %s' % env.user
    run(cmd)

    # zsh configuration file
    put('templates/zshrc', '.zshrc')

    print(green('If the shell does not change, restart your session.'))
