from yaml import safe_load
from collections import namedtuple
from os.path import join, dirname, abspath


class SiteConfig:
    """
    Manage configurations as per the environment
    """

    def __init__(self, config_file='default.yaml'):
        self.config = None
        self.config_file = config_file

        if config_file.startswith('/') is False:
            self.config_file = join(dirname(abspath(__file__)), config_file)

        with open(self.config_file, 'rt') as f:
            self.config = safe_load(f.read())

    def get_config(self):
        """
        Get all configuration
        :return:
        """
        return self.config

    def get_secrets(self):
        """
        Get all secrets
        :return:
        """
        secrets = namedtuple('secrets', 'secrets')
        return secrets(self.config['secrets'])

    def get_secret_key(self):
        """
        Get apps secret key
        :return:
        """
        try:
            return self.config['secrets']['SECRET_KEY']
        except (ValueError, IndexError, TypeError):
            raise ValueError("Invalid server configuration file ({})."
                             .format(self.config_file))
