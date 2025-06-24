import os

class Config:
    # Flask settings
    DEBUG = True
        
    # CSV settings
    CSV_DIR = '.'

    # Display settings
    DEFAULT_MAX_ROWS = 10
    MAX_ROWS_LIMIT = 1000
    
    # Error types for filtering
    ERROR_TYPES = [
        'AttributeError', 'TypeError', 'ValueError', 'KeyError', 'IndexError', 'AssertionError', 'RuntimeError', 'Exception',
        'ImportError', 'FileNotFoundError', 'OSError', 'UnicodeDecodeError', 'NotImplementedError', 'ModuleNotFoundError',
        'OperationalError', 'UnboundLocalError', 'IOError', 'subprocess.CalledProcessError', 'UnicodeEncodeError', 'NameError',
        'RecursionError', 'ZeroDivisionError', 'PermissionError', 'dvc.exceptions.RemoteCacheRequiredError',
        'botocore.exceptions.ClientError', 'sqlite3.OperationalError', 'pydantic.error_wrappers.ValidationError',
        'bleak.exc.BleakError', 'ConnectionResetError', 'SystemError', 'SyntaxError', 'BrokenPipeError',
        'json.decoder.JSONDecodeError', 'sphinx.errors.SphinxWarning'
    ] 