from fabric.api import task, run, env, put
from fabric.colors import green, red
from fabric.context_managers import settings, hide

from deb_handler import apt_install


@task
def install():
    """ Installs and sets zsh as default shell """
    # install zsh
    apt_install('zsh')

    # install zsh examples
    apt_install('zsh-lovers')

    # set as default shell for the user
    print(green('Re-enter your password to set zsh as default.'))
    with settings(hide('warnings'), warn_only=True):
        cmd = 'chsh -s /bin/zsh %s' % env.user
        while True:  # prompt password until success
            if not run(cmd).failed:
                break
            else:
                print(red('Wrong password, try again.'))

    # zsh configuration file
    put('fabfile/templates/zshrc', '.zshrc')

    # zsh fabric autocomplete
    put('fabfile/templates/zsh_fab', '.zsh_fab')

    print(green('If the shell does not change, restart your session.'))
