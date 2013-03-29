import os

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')


MEMCACHE = {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'LOCATION': os.environ.get('MEMCACHIER_SERVERS', ''),
    'TIMEOUT': 500,
    'BINARY': True,
}


DEV_MEMCACHE = {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'LOCATION': '127.0.0.1:11211',
    'TIMEOUT': 500,
}
