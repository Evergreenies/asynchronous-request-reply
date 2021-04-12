from flask import request
from flask_restful import Resource

from producer import queueing, utils, logger


class FirstApp(Resource):
    """Temporary resource for API testing."""

    def post(self):
        """HTTP method `POST` to register job in queue."""
        try:
            requested_payload = request.get_json(force=True)
            massage_token = queueing.register(utils.greetings.__name__,
                                              requested_payload.get('service_name'),
                                              requested_payload)
            return {"message_token": massage_token}, 202
        except Exception as e:
            logger.log_exception(msg=str(e))


class QueuedTasks(Resource):
    """Get jobs exist in Hash Table."""

    def get(self):
        """HTTP method `GET` to get all jobs from queue and Hash Table."""
        return {
            'pending_jobs': queueing.all_pending_jobs(),
            'hash_table': queueing.hash_table()
        }


class JobPooling(Resource):
    """Pooling to check the jobs are completed or not.
    If competed the forward output to consumer service.
    """

    def post(self):
        """HTTP method `POST` to perform provided job."""
        data = request.get_json(force=True)
        logger.log_info(msg=f'Processing - {data.get("massage_token")}.')
        status = queueing.pool_jobs(data.get('service_name'),
                                    data.get('massage_token'))
        return 'Ok', status
