# This config will be copied on first launch.
# Edit the the copied file at '~/.config/dsst/server.json' before launching the server
# IMPORTANT: For a client to access the server you have to set authentication tokens in the server config
DEFAULT_CONFIG = {
    'database': {
        'db_name': 'dsst',
        'user': 'dsst',
        'password': 'dsst'
    },
    'server': {
        'port': 55225,
        'buffer_size': 1024
    },
    'tokens': {
        'readonly': [],
        'readwrite': []
    },
    'logging': dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'file': {'format': '[%(levelname)s] %(asctime)s - %(message)s',
                     'datefmt': '%Y-%m-%d %H:%M:%S'},
            'std': {'format': '[%(levelname)s] %(message)s'}
        },
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'std',
                'level': 'INFO'
            },
            'logfile': {
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 3145728,
                'backupCount': 1,
                'formatter': 'file',
                'level': 'INFO'
            }

        },
        root={
            'handlers': ['console', 'logfile'],
            'level': 'INFO'
        })
}
