import json
import threading

from typing import List, Dict, Tuple, AnyStr, Iterator

from ._utils import generate_token, return_job_result
from .queue import QueueManager
from .hash import HashTableStorage, ProcessStatus
from producer import utils


class Jobs(object):
    """Job execution.
    Once request received it will hit to `register` method and add
    job in Queue as well as in Hash Table
    """

    def __init__(self):
        self.__queue = QueueManager()
        self.__hash = HashTableStorage()

    def register(self, func: str, service_name: str, data: dict) -> str:
        """
        It will enqueued job in Queue and returns `message_token`
        with started function execution.

        :param func: function to execution which will be exist in
        `utils` module.
        :type func: str
        :param service_name: name of the service
        :type service_name: str
        :param data: data received from request parameters
        :type data: dict
        :return: `message_token`
        :rtype: str
        """
        message_token = generate_token()
        self.__queue.enqueue(message_token)
        kwd = {'message_token': message_token}
        self.__hash.set_item(service_name, data, **kwd)
        threading.Thread(target=self.start, args=(func, service_name, data)).start()
        return message_token

    def start(self, func: str, service_name: str, data: dict):
        """
        Picks up job for `func` execution and adding result
        to the Hash Table with a status.

        :param func: function to execution which will be exist in
        `utils` module.
        :type func: str
        :param service_name: name of the service
        :type service_name: str
        :param data: data received from request parameters
        :type data: dict
        :return: `message_token`
        :rtype: str
        """
        message_token = self.__queue.dequeue()
        try:
            if hasattr(utils, func):
                data['result'] = getattr(utils, func)(data)
                data['status'] = ProcessStatus.COMPLETE
                data['message_token'] = message_token
                self.__hash.set_item(service_name, data)
        except Exception as e:
            from producer import logger
            logger.log_exception(f'{e} while execution of job - '
                                 f'{message_token}. Marking job as '
                                 f'failed.')
            data['status'] = ProcessStatus.FAILED
            data['message_token'] = message_token
            self.__hash.set_item(service_name, data)

    def is_completed(self, service_name: str, message_token: str) -> Tuple[AnyStr, Dict]:
        """
        Check whether job completed or not.
        :param service_name: name of the service
        :type service_name: str
        :param message_token: message_token
        :type message_token: str
        :return: (status, job result)
        :rtype: tuple(int, dict)
        """
        return self.__hash.status(service_name, message_token)

    def all_pending_jobs(self) -> List[str]:
        """
        Fetch all pending jobs from Queue.
        :return: list of jobs
        :rtype: list
        """
        return self.__queue.queue

    def hash_table(self) -> List[Tuple[AnyStr, Dict]]:
        """
        Return all jobs exist in Hash Table.
        :return: list of tuples
        :rtype: List[Tuple[AnyStr, Dict]]:
        """
        return self.__hash.hash_table

    @staticmethod
    def get_completed_jobs(queued_jobs: List[Tuple[AnyStr, Dict]]) -> Iterator[Tuple[AnyStr, Dict]]:
        """
        Generator which yields completed jobs.
        :param queued_jobs: list of all jobs fetched from Hash Table
        :type queued_jobs: list of tuples
        :return:
        :rtype:
        """
        try:
            for jb1 in queued_jobs:
                if jb1[1].get('status') == ProcessStatus.COMPLETE:
                    yield jb1
        except Exception as e:
            print('Jobs.get_completed_jobs', e)

    def service_wise_hash(self, service_name: str) -> None:
        """
        Returns all job results for particular service.
        :param service_name:
        :type service_name:
        :return:
        :rtype:
        """
        from producer import logger
        try:
            index = self.__hash.hashed_index().get(service_name)
            if not index:  # Skip execution if jobs does not exists for service
                logger.log_info(msg=f'No more jobs exist for service - {service_name}.')
                return
            qd_jobs = self.__hash.hash_table[index]
            for jb in self.get_completed_jobs(qd_jobs):
                if jb and jb[1]:
                    temp_jd = jb[1].get('redirect_location')
                    response = return_job_result(
                        method=temp_jd.get('method'),
                        url=temp_jd.get('url'),
                        json=json.dumps(jb[1])
                    )
                    if response.status_code == 200:
                        # Delete item from Hash Table if result redirected to desired location
                        self.__hash.delete_item(service_name, jb[1].get('message_token'))
        except Exception as e:
            logger.log_exception(msg=str(e))

    def pool_jobs(self, service_name: str, message_token: str) -> int:
        """
        Executes single job for service and redirects result.
        :param service_name: name of service
        :type service_name: str
        :param message_token: `message_token`
        :type message_token: str
        :return: status
        :rtype: int
        """
        from producer import logger
        try:
            status, value = self.is_completed(service_name, message_token)
            if status == ProcessStatus.COMPLETE:  # Proceed further if job completed execution
                temp_jd = value.get('redirect_location')
                response = return_job_result(
                    method=temp_jd.get('method'),
                    url=temp_jd.get('url'),
                    json=json.dumps(value)
                )
                if response.status_code == 200:
                    # Delete item from Hash Table if result redirected to desired location
                    self.__hash.delete_item(service_name, value.get('message_token'))
                    return 302  # Processed and redirect
            else:
                if status:
                    logger.log_error(msg=f'The job - {message_token} for service - {service_name}'
                                         f' has still status - {status}.')
                else:
                    logger.log_error(msg=f'The job - {message_token} for service - {service_name}'
                                         f' is not found.')
                return 404  # Not not found
        except Exception as e:
            logger.log_exception(msg=str(e))
        return 202  # Accepted
