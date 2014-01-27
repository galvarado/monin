from fabric.api import *
from fabric.context_managers import hide

def staging():
    # Config to deploy staging
    env.enviroment = 'staging'
    env.branch = 'staging'
    env.push_code = True
    env.collect_static = False
    env.resetdb = False
    env.syncdb = True
    setup()


def production():
    # Config to deploy production
    env.enviroment = 'production'
    env.branch = 'master'
    env.push_code = True
    env.collect_static = True
    env.resetdb = False
    env.syncdb = False
    setup()


def setup():
    with hide('running', 'stdout', 'stderr'):

        # Get the app directory
        env.app_directory = local("""
            while [ ! -e "fabfile.py" ]; do
                cd ..
            done
            manage_file=$(find . | grep manage.py | grep -v lib  | grep -v build | head -1);
            echo ${manage_file%manage.py}
        """, capture=True)

        # Get the app name from the git remote name
        env.app_name = local("""
            git remote -v | grep ^{enviroment} | head -1 | cut -d":" -f2 | cut -d"." -f1
        """.format(**env), capture=True)

    env.managepy = '{app_directory}manage.py'.format(**env)


def push_code(branch=None):
    if branch is not None:
        env.branch = branch
    command = 'git push --force {enviroment} {branch}:master'.format(**env)
    local(command)


def resetdb():
    command = 'heroku pg:reset DATABASE --confirm {app_name}'.format(**env)
    local(command)


def syncdb():
    command = 'heroku run python {managepy} syncdb --noinput --app={app_name}'.format(**env)
    local(command)

def collect_static():
    command = 'heroku run python {managepy} collectstatic --noinput --app={app_name}'.format(**env)
    local(command)


def deploy(branch=None):
    # Pushing code to heroku
    if env.push_code:
        push_code(branch)

    # Resetting database
    if env.resetdb:
        resetdb()

    # Syncing database
    if env.syncdb:
        syncdb()

    # Collecting static files
    if env.collect_static:
        collect_static()