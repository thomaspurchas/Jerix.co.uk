from fabric.api import local
from fabric.context_managers import shell_env

def set_aws():
    local('export AWS_ACCESS_KEY_ID=AKIAITZEJLE7PSX5ALOQ')
    local('export AWS_SECRET_ACCESS_KEY=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')

def push():
    local('git push')

def stage_deploy():
    local('git push heroku-staging -f')
    local('STAGING=TRUE ./manage.py compress')
    local('STAGING=TRUE DEBUG=false ./manage.py collectstatic --noinput')
    local('heroku restart --app jerix-staging')
    local('rm -rf ../static')
    
def stage_migrate():
    stage()
    local('heroku run jerix.co.uk/eso/manage.py syncdb --app jerix-staging')
    local('heroku run jerix.co.uk/eso/manage.py migrate --app jerix-staging')
 
def stage_update_index():
    local('heroku run jerix.co.uk/eso/manage.py update_index --remove --app jerix-staging')    
   
def deploy(stage=True):
    if stage: stage_deploy()
    local('git push heroku -f')
    local('DEBUG=false ./manage.py compress')
    local('DEBUG=false ./manage.py collectstatic --noinput')
    local('heroku restart --app jerix')
    local('rm -rf ../static')
    
def migrate():
    stage_migrate()
    deploy(False)
    local('heroku run jerix.co.uk/eso/manage.py syncdb --app jerix')
    local('heroku run jerix.co.uk/eso/manage.py migrate --app jerix')

def update_index():
    local('heroku run jerix.co.uk/eso/manage.py update_index --remove --app jerix')