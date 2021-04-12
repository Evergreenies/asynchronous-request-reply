import json
import requests

from flask import Flask, request

from _queue import QueueManager
from _periodic_caller import set_interval

app = Flask(__name__)
jobs = QueueManager()

_SERVICE_NAME = 'greeting'
_PRODUCER_SERVICE = 'http://127.0.0.1:8000/'
_CURRENT_SERVICE = 'http://127.0.0.1:8001/'


@app.route('/call-me', methods=['POST'])
def call_me():
    data = request.get_json(force=True)
    data.update({
        'service_name': _SERVICE_NAME,
        'redirect_location': {
            'url': f'{_CURRENT_SERVICE}jobs-result',
            'method': 'POST'
        }
    })
    response = requests.request(
        method='POST',
        url=f'{_PRODUCER_SERVICE}v1/submit-job',
        headers={
            'Content-Type': 'application/json'
        },
        json=data
    )
    data, status_code = response.json(), response.status_code

    # Insert job in queue if status_code is 202 (Accepted)
    if status_code == 202:
        jobs.enqueue(data.get('message_token'))

    return json.dumps(data), status_code


@app.route('/jobs-result', methods=['POST'])
def response_returned():
    """
    This function handles request for job completed.

    :return: status of request
    :rtype: tuple(str, int)
    """
    response = request.get_json(force=True)
    print("After Job Complete: ", response)
    return 'Ok', 200


@app.before_first_request
@set_interval(15)
def polling():
    """
    Function performs like worker pool to check whether job completed or not
    If job not completed then it will again enqueues that job to queue.

    :return:
    :rtype: None
    """
    print("Pooling . . .")
    try:
        pending_jobs = []
        while jobs:
            job = jobs.dequeue()
            data = {
                'service_name': _SERVICE_NAME,
                'massage_token': job
            }
            response = requests.request(
                method='POST',
                url=f'{_PRODUCER_SERVICE}v1/pool-job',
                headers={
                    'Content-Type': 'application/json'
                },
                json=data
            )
            data, status_code = response.json(), response.status_code
            # If status 302 means job competed and returned response to the caller
            if status_code == 202:
                # Save job which hasn't completed yet.
                pending_jobs.append(job)

        for job in pending_jobs:
            jobs.enqueue(job)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
