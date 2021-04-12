from flask import Blueprint

from producer import app, api

# Blueprint for process_controller
process_controller_blueprint = Blueprint('first_app', __name__)

# Add REST-API in Blueprint
api.blueprint_setup = process_controller_blueprint
api.blueprint = process_controller_blueprint

from producer.first_app import api_endpoints

# Registered Blueprints
app.register_blueprint(process_controller_blueprint, url_prefix='/v1')
