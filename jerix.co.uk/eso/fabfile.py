from fabric.api import local
from fabric.context_managers import shell_env

def set_aws():
    local('export AWS_ACCESS_KEY_ID=AKIAITZEJLE7PSX5ALOQ')
    local('export AWS_SECRET_ACCESS_KEY=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')

def stage():
    local('git push heroku-staging -f')
    local('STAGING=TRUE DEBUG=false ./manage.py compress')
    local('STAGING=TRUE DEBUG=false ./manage.py collectstatic --noinput')
    local('rm -rf ../static')
    
def deploy():
    stage()
    local('git push heroku -f')
    local('DEBUG=false ./manage.py compress')
    local('DEBUG=false ./manage.py collectstatic --noinput')
    local('rm -rf ../static')

    