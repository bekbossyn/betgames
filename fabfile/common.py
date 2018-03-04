from fabric.decorators import task
from fabric.operations import sudo, run


@task
def apt_get_update():
    """
    Runs 'apt-get update' command on remote machine
    """
    sudo('apt-get update')


@task
def apt_get(*packages):
    """
    Runs apt-get install command for all provided packages
    """
    sudo('apt-get -y -f install %s' % ' '.join(packages), shell=False)


@task
def git_pull():
    """
    Updates the repository
    """
    run("cd /home/betgames/; git pull")


@task
def update():
    """
    Restarts server
    """
    run("cd /home/betgames/; bash run.sh")
