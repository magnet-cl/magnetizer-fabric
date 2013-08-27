from fabric.api import task, run, env, put, prompt
from fabric.colors import green, red
from fabric.context_managers import settings, hide
from fabric.contrib.files import upload_template, exists, sed
from fabric.contrib.console import confirm
from fabtools.deb import update_index
from os import listdir
from os.path import join
from os.path import abspath
from os.path import dirname

from git import git_clone, git_install
import utils

root_folder = dirname(abspath(__file__))


@task
def install():
    """ Installs and sets zsh as default shell """
    # update apt index
    update_index(quiet=False)

    # install zsh
    utils._deb.install('zsh')

    # set as default shell for the user
    print(green('Re-enter your password to set zsh as default.'))
    with settings(hide('warnings'), warn_only=True):
        cmd = 'chsh -s /bin/zsh %s' % env.user
        while True:  # prompt password until success
            if not run(cmd).failed:
                break
            else:
                print(red('Wrong password, try again.'))

    # install git if is not available
    git_install()

    # install oh-my-zsh
    if not exists('~/.oh-my-zsh'):
        git_clone('git://github.com/robbyrussell/oh-my-zsh.git',
                  '~/.oh-my-zsh')

    # zsh configuration
    configure()


@task
def update():
    """ Updates oh-my-zsh and custom themes. """
    # update oh-my-zsh
    cmd = '/usr/bin/env ZSH=~/.oh-my-zsh /bin/sh ~/.oh-my-zsh/tools/upgrade.sh'
    run(cmd)

    # update custom files
    upload_custom_files()


@task
def upload_custom_files():
    """ Uploads custom files for oh-my-zsh. """

    themes_folder = '{}/zsh-themes'.format(root_folder)
    plugins_folder = '{}/zsh-plugins'.format(root_folder)
    custom_folder = '~/.oh-my-zsh/custom'

    # custom themes
    for theme in listdir(themes_folder):
        print('Uploading %s...' % theme)
        put('%s/%s' % (themes_folder, theme), custom_folder)

    print(green('To set your zsh theme, you must change the ZSH_THEME '
                'environment variable in ~/.zshrc'))

    # custom plugins
    for plugin in listdir(plugins_folder):
        plugin_subfolder = plugin.split('.')[0]
        destination_folder = join(custom_folder, "plugins", plugin_subfolder)
        if not exists(destination_folder):
            cmd = 'mkdir -p %s' % destination_folder
            run(cmd)
        print('Uploading %s...' % plugin)
        put('%s/%s' % (plugins_folder, plugin), destination_folder)


@task
def install_theme(theme=None):

    themes = ['powerline', 'miloshadzic-3-path', 'miloshadzic-full-path']

    if theme not in themes:
        print "Theme not found. Example: zsh.install_theme:powerline"
        print "List of themes: "
        print "    powerline"
        print "    miloshadzic-3-path"
        print "    miloshadzic-full-path"

        return

    upload_custom_files()

    print(green('Setting zsh theme: %s' % theme))
    sed('~/.zshrc', "^ZSH_THEME=[\"][a-zA-Z0-9-]*[\"]", 'ZSH_THEME="%s"' %
        theme)

    if theme == "powerline":
        font_folder = "~/.fonts/"
        if not exists(font_folder):
            run('mkdir -p %s' % font_folder)

        print(green('Downloading fonts'))
        run("wget -O %sPowerlineSymbols.otf 'https://github.com/Lokaltog/"
            "powerline/raw/develop/font/PowerlineSymbols.otf'" % font_folder)

        font_config_folder = "~/.fonts.conf.d/"
        if not exists(font_config_folder):
            run('mkdir -p %s' % font_config_folder)

        print(green('Downloading fonts config file'))
        file_name = "%s10-powerline-symbols.conf" % font_config_folder

        run("wget -O %s 'https://github.com/Lokaltog/powerline/raw/develop/"
            "font/10-powerline-symbols.conf'" % file_name)

        print(green('Updating fonts Cache'))
        run("fc-cache -vf %s" % font_folder)


@task
def configure():
    """ Configures the zshrc file. """

    install_autojump = False

    # plugins configuration
    plugins = []
    recommended_plugins = (['git', 'github', 'git-flow', 'heroku',
                           'last-working-dir', 'pip', 'autojump',
                            'command-not-found', 'debian', 'encode64',
                            'vagrant', 'ruby', 'colored-man', 'grepr',
                            'mclone'])
    recommended_plugins.sort()
    for plugin in recommended_plugins:
        if confirm('Would you like to use the %s plugin?' % plugin):
            plugins.append(plugin)
            if plugin == "autojump":
                install_autojump = True

    plugins = ' '.join(plugins)

    # default editor
    editor = prompt('Please specify your default editor', default='vim')

    context = {
        'plugins': plugins,
        'default_editor': editor,
        'user': env.user
    }
    upload_template('{}/templates/zshrc'.format(root_folder), '.zshrc',
                    context=context)

    # zsh fabric autocomplete
    put('{}/templates/zsh_fab'.format(root_folder), '.zsh_fab')

    # upload custom files
    upload_custom_files()

    if install_autojump:
        utils._deb.install('autojump')

    print(green('If the shell does not change, restart your session.'))
