""" Magnetizer Tasks """
import os.path

from fabfile import ssh
assert ssh

from fabfile import zsh
assert zsh

from fabfile import vim
assert vim

from fabfile import ruby
assert ruby

from fabfile import rxvt
assert rxvt

from fabfile import tmux
assert tmux

from fabfile import node
assert node

from fabfile import nginx
assert nginx

from fabfile import admin
assert admin

from fabfile import postgresql
assert postgresql

""" fabric global configuration """

from fabric.api import env

# support ssh_config
if os.path.isfile('~/ssh.config'):
    env.use_ssh_config = True
