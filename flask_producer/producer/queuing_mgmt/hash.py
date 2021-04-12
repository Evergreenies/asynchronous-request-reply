from abc import ABC, abstractmethod
from typing import Dict, Tuple, AnyStr


class ProcessStatus(object):
    """Job status"""
    NOT_EXIST = -1
    FAILED = 0
    CREATED = 1
    PROCESSING = 2
    COMPLETE = 3
    ACCEPTED = 4


class Hash(ABC):
    """Abstract class for Hash"""

    @abstractmethod
    def hash_function(self, service_name: str) -> int:
        """Method to generate hash key."""
        pass

    @abstractmethod
    def set_item(self, service_name: str, data: dict, **kwargs: dict) -> str:
        """Insert element in Hash Table."""
        pass

    @abstractmethod
    def get_item(self, service_name: str, message_token: str) -> Tuple[AnyStr, Dict]:
        """Get element from Hash Table."""
        pass

    @abstractmethod
    def has(self, service_name: str, message_token: str) -> bool:
        """Check whether job exists for service or not."""
        pass

    @abstractmethod
    def delete_item(self, service_name: str, message_token: str) -> int:
        """Delete a job from Hash Table."""
        pass


class HashTable(Hash):
    """Hash Table to store jobs as per the service."""

    def __init__(self, size=20):
        self.size = size
        self.hash_table = [[] for _ in range(self.size)]
        self._hash_indexes = {}

    def hashed_index(self) -> dict:
        """
        Returns indexes from Hash Table.

        :return: All Indexes exist in Hash Table.
        :rtype: dict
        """
        return self._hash_indexes

    def hash_function(self, service_name: str) -> int:
        """
        Creates a Hash Table index.

        :param service_name: name of service
        :type service_name: str
        :return: integer index of service
        :rtype: int
        """
        if len(self._hash_indexes) == self.size:  # Expand if Hash Table size is full
            self._expand()

        # Check whether is service index exist in Hash Table. If not exist
        # then create index for service
        if service_name not in list(self._hash_indexes):
            self._hash_indexes[service_name] = len(self._hash_indexes) + 1
        return self._hash_indexes[service_name]

    def has(self, service_name: str, message_token: str) -> bool:
        """
        Check whether job exists for service or not.

        :param service_name: name of service
        :type service_name: str
        :param message_token: `message_token`
        :type message_token: str
        :return: True or False
        :rtype: bool
        """
        if not message_token:  # if `message_token` not nullable
            raise ValueError(f'You must provide `message_token`')

        hash_key = self.hash_function(service_name)
        for index, ele in enumerate(self.hash_table[hash_key]):
            if ele[0] == message_token:
                return True
        return False

    def is_full(self) -> bool:
        """Check whether Hash Table is full or have space."""
        return len(self.hash_table) > self.size

    def set_item(self, service_name: str, data: dict, **kwargs: dict) -> str:
        """
        Set/Update values to the hash table

        :param service_name: name of the service
        :type service_name: str
        :param data: complete data with `message_token` key
        :type data: dict
        :return: `message_token`
        :rtype: str
        """

        if self.is_full():
            self._expand()

        message_token = data.get('message_token')
        generated_message_token = kwargs.get('message_token', message_token)
        hash_key = self.hash_function(service_name)
        exist = False
        if message_token:  # Update if `message_token` matches
            for index, ele in enumerate(self.hash_table[hash_key]):
                if ele[0] == message_token:
                    self.hash_table[hash_key][index] = (message_token, data)
                    exist = True
        if not exist:  # Make new entry if `message_token` not provided of found in Hash Table
            data['message_token'] = generated_message_token
            data['status'] = ProcessStatus.CREATED
            self.hash_table[hash_key].append((generated_message_token, data))

        return message_token

    def get_item(self, service_name: str, message_token: str) -> Tuple[AnyStr, Dict]:
        """
        Get an item from the Hash Table for provided `service_name`.
        :param service_name:
        :type service_name:
        :param message_token:
        :type message_token:
        :return:
        :rtype:
        """
        if not message_token:
            raise ValueError(f'You must provide `message_token`')

        hash_key = self.hash_function(service_name)
        for key, value in self.hash_table[hash_key]:
            if key == message_token:
                return key, value
        return message_token, {}

    def delete_item(self, service_name: str, message_token: str) -> int:
        """
        Delete item from Hash Table for provided `service_name`.

        :param service_name: name of service
        :type service_name: str
        :param message_token: `message_token`
        :type message_token: str
        :return: 0 ot 1
        :rtype: int
        """
        if not message_token:
            raise ValueError(f'You must provide `message_token`')

        hash_key = self.hash_function(service_name)
        for index, item in enumerate(self.hash_table[hash_key]):
            if item[0] == message_token:
                del self.hash_table[hash_key][index]
                return 1
        return 0

    def _expand(self) -> None:
        self.hash_table += [[] for _ in range(self.size)]


class HashTableStorage(HashTable):
    """Utility functions for Hash Table storage."""

    def __init__(self, size=20):
        super().__init__(size)

    def status(self, service_name: str, message_token: str) -> Tuple[int, Dict]:
        """
        Check status of provided 'message_token`

        :param service_name: name of service
        :type service_name: str
        :param message_token: `message_token`
        :type message_token: str
        :return: tuple(status, item value)
        :rtype: tuple(int, dict)
        """
        if not message_token:
            raise ValueError(f'You must provide `message_token`')

        hash_key = self.hash_function(service_name)
        for key, value in self.hash_table[hash_key]:
            if key == message_token:
                return value.get('status'), value
        return ProcessStatus.NOT_EXIST, {}

    def status_update(self, service_name: str, message_token: str, status) -> int:
        """
        Updating status of provided job `message_token`.

        :param service_name:
        :type service_name:
        :param message_token:
        :type message_token:
        :param status:
        :type status:
        :return:
        :rtype:
        """
        if not message_token:
            raise ValueError(f'You must provide `message_token`')

        hash_key = self.hash_function(service_name)
        for index, item in enumerate(self.hash_table[hash_key]):
            if item[0] == message_token:
                self.hash_table[hash_key][index][1]['status'] = status
                return 1
        return 0
