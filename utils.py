import yaml
from typing import Any, Dict
from exceptions import *

def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load the configuration from a YAML file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: The configuration as a dictionary.

    Raises:
        InvalidConfigurationError: If there is an error in the configuration.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        raise InvalidConfigurationError(f"Error loading configuration: {str(e)}")

def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate the configuration.

    Args:
        config (dict): The configuration as a dictionary.

    Raises:
        InvalidConfigurationError: If there is an error in the configuration.
    """
    if 'openai' not in config or 'api_key' not in config['openai'] or 'model' not in config['openai']:
        raise InvalidConfigurationError("Missing 'openai' or 'api_key' or 'model' in configuration")
    if 'refresh_time' not in config:
        raise InvalidConfigurationError("Missing 'refresh_time' in configuration")



def validate_upload(file):
    config = load_config()
    allowed_types = config['allowed_types']
    max_size = config['max_size']
    
    if file.type not in allowed_types:
        raise UploadTypeError()
    if file.size > max_size: 
        raise UploadSizeError()