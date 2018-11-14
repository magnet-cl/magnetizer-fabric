# -*- coding: utf-8 -*-

import os

import click
import sh


@click.command()
@click.option(
    '-t',
    '--task',
    default='-l',
    prompt=True,
    type=click.STRING,
    help='Executes the given task',
)
@click.option(
    '-H',
    '--host',
    default='localhost',
    prompt=True,
    type=click.STRING,
    help='Target host',
)
@click.option(
    '-f',
    '--fabfile',
    type=click.Path(exists=True),
    help='Specify the fabric config parent path',
)
def cli(task, host, fabfile):
    click.secho('Magnetizer', fg='cyan')

    # store the current working directory
    current_dir = os.getcwd()

    # change the current working directory to magnetizer
    if not fabfile:
        magnetizer_dir = '{}/.magnetizer'.format(os.path.expanduser('~'))
    else:
        magnetizer_dir = fabfile
    os.chdir(magnetizer_dir)

    click.secho('Fabric version', fg='green')
    print(sh.pipenv.run('fab', '--version'))
    click.secho('Executing {}'.format(task), fg='red')
    sh.pipenv.run(
        'fab',
        task,
        '-H',
        host,
        _fg=True
    )

    # restore the initial working directory
    os.chdir(current_dir)


if __name__ == '__main__':
    cli()
