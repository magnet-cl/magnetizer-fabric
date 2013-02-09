from fabric.api import task, run, env, put, prompt
from fabric.colors import green, red
from fabric.context_managers import settings, hide
from fabric.contrib.files import upload_template
from re import match

from fabtools.deb import update_index
from fabtools.deb import is_installed, install as deb_install
from git import git_clone


@task
def install():
    """ Installs and sets zsh as default shell """
    # update apt index
    update_index(quiet=False)

    # install zsh
    if not is_installed('zsh'):
        deb_install('zsh')

    # install zsh examples
    if not is_installed('zsh-lovers'):
        deb_install('zsh-lovers')

    # set as default shell for the user
    print(green('Re-enter your password to set zsh as default.'))
    with settings(hide('warnings'), warn_only=True):
        cmd = 'chsh -s /bin/zsh %s' % env.user
        while True:  # prompt password until success
            if not run(cmd).failed:
                break
            else:
                print(red('Wrong password, try again.'))

    # install oh-my-zsh
    git_clone('git://github.com/robbyrussell/oh-my-zsh.git', '~/.oh-my-zsh')

    # zsh configuration file: plugins
    plugins = []
    recommended_plugins = (['git', 'github', 'git-flow', 'heroku',
                           'last-working-dir', 'pip', 'autojump',
                            'command-not-found', 'debian', 'encode64',
                            'vagrant', 'ruby'])
    recommended_plugins.sort()
    for plugin in recommended_plugins:
        input = prompt('Would you like to use the %s plugin?'
                       % plugin, default='Y')
        if match('Y|y', input):
            plugins.append(plugin)
    plugins = ' '.join(plugins)

    # zsh configuration file: default editor
    editor = prompt('Please specify your default editor', default='vim')

    context = {
        'plugins': plugins,
        'default_editor': editor,
        'user': env.user
    }
    upload_template('fabfile/templates/zshrc', '.zshrc', context=context)

    # zsh fabric autocomplete
    put('fabfile/templates/zsh_fab', '.zsh_fab')

    print(green('If the shell does not change, restart your session.'))
