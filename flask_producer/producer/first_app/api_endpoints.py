from producer import api
from producer.first_app.resources import (
    FirstApp, QueuedTasks, JobPooling)

api.add_resource(FirstApp, '/submit-job')
api.add_resource(QueuedTasks, '/jobs')
api.add_resource(JobPooling, '/pool-job')
