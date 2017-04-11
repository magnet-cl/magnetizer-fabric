import platform

from fabric.api import task, run, env, put, prompt, cd
from fabric.colors import green, red
from fabric.context_managers import settings, hide
from fabric.contrib.files import upload_template, exists, sed, contains
from fabric.contrib.console import confirm
from os import listdir
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import basename

from fabfile.git import git_clone, git_install
from fabfile import utils

ROOT_FOLDER = dirname(abspath(__file__))




@task
def install():
    """ Installs and sets zsh as default shell """
    # update apt index
    update_index(quiet=False)

    # install zsh
    utils.os_commands.install('zsh')

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

    themes_folder = '{}/zsh-themes'.format(ROOT_FOLDER)
    plugins_folder = '{}/zsh-plugins'.format(ROOT_FOLDER)
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

        github_url = "https://github.com/"
        repo_url = "Lokaltog/powerline-fonts/blob/master/UbuntuMono/"
        url = "%s%s" % (github_url, repo_url)

        with cd('.fonts'):
            def download_font(font):
                file_url = "%s%s" % (url, font.replace(' ', "%20"))
                file_name = font.replace(' ', "\ ")
                cmd = "wget -O %s '%s?raw=true'" % (file_name, file_url)
                run(cmd)

            download_font("Ubuntu Mono derivative Powerline Bold Italic.ttf")
            download_font("Ubuntu Mono derivative Powerline Bold.ttf")
            download_font("Ubuntu Mono derivative Powerline Italic.ttf")
            download_font("Ubuntu Mono derivative Powerline.ttf")

        utils.os_commands.install('fontconfig')
        print(green('Updating fonts Cache'))
        run("fc-cache -vf %s" % font_folder)


@task
def install_plugins(*plugins):
    install_autojump = False

    destination_folder = '~/.zsh'

    if not exists(destination_folder):
        run('mkdir -p %s' % destination_folder)

    plugins_file = '{}/plugins.zsh'.format(destination_folder)

    if not exists(plugins_file):
        upload_template(
            '{}/templates/oh-my-zsh-plugins'.format(ROOT_FOLDER),
            '{}/plugins.zsh'.format(destination_folder),
            context={}
        )

    plugins_to_install = []

    for plugin in plugins:
        if plugin == "autojump":
            install_autojump = True

        if not contains(plugins_file, plugin):
            plugins_to_install.append(plugin)

    if plugins_to_install:
        sed(plugins_file, '\)', ' {})'.format(' '.join(plugins_to_install)))

    if install_autojump:
        utils.os_commands.install('autojump')


@task
def configure_plugins():
    plugins = []

    recommended_plugins = (['git', 'github', 'git-flow', 'pip', 'autojump',
                            'command-not-found', 'encode64',
                            'ruby', 'colored-man', 'grepr', 'mclone', 'cdenv',
                            'findm', 'history-substring-search', 'capistrano'])

    if platform.system().lower() == 'linux':
        recommended_plugins.append('debian')

    recommended_plugins.sort()
    for plugin in recommended_plugins:
        if confirm('Would you like to use the %s plugin?' % plugin):
            plugins.append(plugin)

    install_plugins(*plugins)


@task
def configure():
    """ Configures the zshrc file. """

    # plugins configuration
    configure_plugins()

    # default editor
    editor = prompt('Please specify your default editor', default='vim')

    context = {
        'default_editor': editor,
        'user': env.user
    }
    upload_template('{}/templates/zshrc'.format(ROOT_FOLDER), '.zshrc',
                    context=context)

    # zsh fabric autocomplete
    put('{}/templates/zsh_fab'.format(ROOT_FOLDER), '.zsh_fab')

    # upload custom files
    upload_custom_files()

    print(green('If the shell does not change, restart your session.'))


@task
def install_flavor(flavor='default'):
    """ Uploads flavor files for zsh."""

    zsh_flavor_folder = '{}/../flavors/{}/zsh'.format(ROOT_FOLDER, flavor)
    destination_folder = '~/.zsh'

    # custom themes
    for flavor_file in listdir(zsh_flavor_folder):
        print(green('Uploading %s...' % basename(flavor_file)))
        put('{}/{}'.format(zsh_flavor_folder, flavor_file), destination_folder)
