# Magnetizer

http://magnet-cl.github.io/magnetizer/

## Description
At Magnet we use Magnetizer to quickly setup the terminal in local and remote Linux machines. This includes a complete configuration of zsh, vim.
It also comes with other tools:

    * SSH: Super easily generate and add ssh keys to a remote host
* Ruby: Install Ruby and Ruby on Rails with 

    Magnetizer uses python's Fabric tools to run tasks on remote (and local) machines.

## Installation

Run `./install.sh`.

## Usage
You have a list of commands you can execute in you local machine or a remote one. To print the list of available tasks type `fab -l`.

Each task must be ran as follows:

`fab <task>`

You need to specify the target machine, so it will ask you for the host in which you wish to run the task and assume your user is you current terminal user.

You can override this behaviour using the H parameter:

`fab -H <user>@<host> <task>`

You can also concatenate commands:

`fab -H <user>@<host> <task1> <task2>`

### Examples
To get zsh installed and set as the default shell on your local machine, you should ran:

`fab -H <user>@localhost zsh.install `

    A concatenation example could be that you want that your current public key is accepted in your own computer (to speed up Magnetizer calls) and install vim configuration:

`fab -H <user>@localhost ssh.add_authorized_key vim.install`

### Available commands

* `ssh.generate_key`: Generate public and private ssh keys.
* `ssh.add_authorized_key`: Adds your local public key to the authorized keys.
* `zsh.install`: Installs zsh, fully configured.
* `zsh.update`: Updates zsh with the latest Magnetizer configuration.
* `zsh.themes`: Change the theme of zsh
* `vim.install`: Installs vim, fully configured fo maximum programmer efficiency.
* `vim.update`: Updates vim with the latest Magnetizer configuration.
* `vim.restore_backup`: Restores a backup of vim... ehh I don't know what it restores, but I bet it is awesome.
* `ruby.install`: Installs Ruby
* `ruby.install_rails`: Installs Ruby on Rails
