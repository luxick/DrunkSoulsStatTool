# This config will be copied on first launch.
# Edit the the copied file at '~/.config/dsst/server.json' before launching the server
DEFAULT_CONFIG = {
    'database': {
        'db_name': 'dsst',
        'user': 'dsst',
        'password': 'dsst'
    },
    'server': {
        'host': 'localhost',
        'port': 55225,
        'buffer_size': 1024
    },
    'tokens': {
        '<read_write_token_here>': 'rw',
        '<read_only_token_here>': 'r'
    }
}
