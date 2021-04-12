import importlib

from flask import Flask
from flask_restful import Api

# App Initialization
app = Flask(__name__)
app.config.from_object('config')

# Initializing REST API Object
api = Api(app)

from producer.queuing_mgmt.jobs import Jobs
from producer.custom_logger.logger import CustomLogger

queueing = Jobs()

logger = CustomLogger()

for installed_app in app.config.get('INSTALLED_APPS', []):
    try:
        importlib.__import__(installed_app)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f'Module {installed_app} not found!')
