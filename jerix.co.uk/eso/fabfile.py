from fabric.api import local

def deploy():
    local('git push heroku -f')
    local('DEBUG=false ./manage.py compress')
    local('DEBUG=false ./manage.py collectstatic --noinput')
    local('rm -rf ../static')