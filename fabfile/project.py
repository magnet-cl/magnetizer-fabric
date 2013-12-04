import admin
import ssh
import node
import zsh
import vim

from fabric.api import task


@task
def set_django_environment():
    """ Assumes that the user exists and it's sudo """
    ssh.add_authorized_key()
    admin.sudo_without_password()
    node.install()
    zsh.install()
    vim.install()
