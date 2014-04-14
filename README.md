# Magnetizer

http://magnet-cl.github.io/magnetizer/

## Description
At Magnet we use Magnetizer to quickly setup the terminal in local and remote
Linux machines. The tasks included are listed in the [available
commands](#available-commands) section.

Magnetizer uses python's Fabric tools to run tasks on remote (and local)
machines. Since Fabric works over SSH, Magnetizer is configured to load the
settings present in the ssh config file, for instance, hostname aliases.

## Installation

Run `./install.sh`.

## Usage
You have a list of commands you can execute in your local machine or a remote
one. To print the list of available tasks type:

`fab -l`.

Each task must be ran as follows:

`fab <task>`

You can get the description of a task with the -d parameter:

`fab -d <task>`

You need to specify the target machine, so it will ask you for the host in
which you wish to run the task and assume your user is your current terminal
user.

You can override this behaviour using the H parameter:

`fab -H <user>@<host> <task>`

You can also concatenate commands:

`fab -H <user>@<host> <task1> <task2>`

### Examples
To get zsh installed and set as the default shell on your local machine, you
should run:

`fab -H <user>@localhost zsh.install `

A concatenation example could be that you want that your current public key is
accepted in your own computer (to speed up Magnetizer calls) and install vim
configuration:

`fab -H <user>@localhost ssh.add_authorized_key vim.install`

## Server initial configuration
In order to configure a new server (usually a VPS), you must run the
following sequence of commands:

1. Add `<user>` with `sudo` as extra group: `fab admin.add_user:<user>,sudo -H
root@host`
1. Allow sudoers without password: `fab admin.sudo_without_password -H
root@host`
1. Disable password authentication: `fab ssh.disable_password_authentication
-H root@host`
1. Disable root login: `fab ssh.disable_root_login -H root@host`
1. Add your public ssh key to the authorized keys: `fab
ssh.add_authorized_key -H <user>@host` (Please notice that this command must
be run giving the user previously created).
1. Reloads SSH configuration: `fab ssh.reload_configuration root@host`

Afterwards, we strongly recommend you to install zsh and vim through the tasks
provided.

## Available commands

    * admin.add_user: Adds user, its group can also be specified.
    * nginx.install_passenger: Installs nginx with passenger support.
    * node.install: Installs node.
    * postgresql.install: Installs PostgreSQL and its development packages.
    * ruby.install: Installs Ruby.
    * ruby.install_rails: Installs Ruby on Rails.
    * ruby.install_wirble: Improves irb console.
    * ssh.add_authorized_key: Adds your local public key to the authorized
      keys.
    * ssh.disable_password_authentication: Disables password authentication.
    * ssh.disable_root_login: Disables root login authentication.
    * ssh.generate_key: Generates public and private ssh keys.
    * tmux.configure: Uploads the tmux configuration file.
    * tmux.install: Installs and configure tmux.
    * vim.install: Installs vim, fully configured fo maximum programmer
      efficiency.
    * vim.restore_backup: Restores vim to a pre-magnetizer configuration if
      available.
    * vim.update: Updates vim with the latest Magnetizer configuration.
    * zsh.configure: Deploys the configuration file asking some preferences.
    * zsh.install: Installs zsh, fully configured.
    * zsh.update: Updates zsh with the latest Magnetizer configuration.
