import os
from configparser import ConfigParser
from .encryption_tools import decrypt_message

INI_KEY = os.getenv('INI_KEY')  # Make sure this is in your ~/.bashrc
assert INI_KEY, 'No INI_KEY'


# Functions included in this file:
# # postgres_connection
# # heroku_postgres_connection


def postgres_connection(database=None,
                        section='postgres', cfg_path='conf/cred.ini'):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    username, password, host, port = (
        decrypt_message(cfg.get(section, key), INI_KEY)
        for key in ['username', 'password', 'host', 'port']
    )

    if database:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'
    else:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}'

    return connection_uri


def heroku_postgres_connection(section='heroku-postgres', cfg_path='conf/cred.ini'):
    """Given an INI file with a ['heroku-postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port', 'db_name']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    username, password, host, port, database = (
        decrypt_message(cfg.get(section, key), INI_KEY)
        for key in ['username', 'password', 'host', 'port', 'db_name']
    )

    connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'

    return connection_uri
