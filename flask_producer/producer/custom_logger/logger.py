import os
import yaml
import logging
import logging.config

from producer import app


class CustomLogger:
    """Handler which handles applications state."""

    def __init__(self, log_dir=app.config.get('ROOT_PATH'),
                 file_prefix=app.name):
        """
        Logging initializer.
        """
        prefix = '{}_'.format(file_prefix) if file_prefix is not None else ''
        logging.config.dictConfig(self.configure(prefix, log_dir))
        self.logger = logging.getLogger(app.name)

    def configure(self, prefix, log_dir):
        """Logger configuration."""
        path = os.path.abspath(__file__)
        config_file = os.path.join(os.path.dirname(path), 'logging.yaml')
        try:
            assert os.path.exists(config_file), \
                'Configuration file for Logging does not exist.'
            with open(config_file, 'rt') as f:
                config = yaml.safe_load(f.read())
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                abs_dir_path = os.path.abspath(log_dir)

                for key, val in config.items():
                    if key == 'handlers':
                        for k, v in val.items():
                            file_name = v.get('filename')
                            if file_name is not None:
                                file_name = '{}{}'.format(prefix, file_name)
                                abs_path = os.path.join(abs_dir_path, file_name)
                                v['filename'] = abs_path

                return config
        except Exception as e:
            print('Error file logging configurations - ', e)

    def __del__(self):
        """Docs not found"""
        pass

    def __enter__(self):
        """Docs not found"""
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Docs not found"""
        pass

    def log_debug(self, msg):
        """Log DEBUG"""
        try:
            self.logger.debug(msg)
        except Exception as e:
            print(e)

    def log_error(self, msg):
        """Log ERROR's"""
        try:
            self.logger.error(msg, exc_info=True)
        except Exception as e:
            print(e)

    def log_info(self, msg):
        """Log INFO"""
        try:
            self.logger.info(msg)
        except Exception as e:
            print(e)

    def log_warning(self, msg):
        """Log WARNING's"""
        try:
            self.logger.warning(msg, exc_info=True)
        except Exception as e:
            print(e)

    def log_critical(self, msg):
        """Log CRITICAL"""
        try:
            self.logger.critical(msg)
        except Exception as e:
            print(e)

    def log_exception(self, msg):
        """Log EXCEPTION's"""
        try:
            self.logger.exception(msg, exc_info=True)
        except Exception as e:
            print(e)

    @staticmethod
    def log_console(msg):
        """Log on CONSOLE"""
        print(msg)

    @staticmethod
    def debug_print(*args):
        """PRINT IF DEBUG=True"""
        try:
            if os.environ["DEBUG"]:
                print(*args)
        except Exception as e:
            print(e)
