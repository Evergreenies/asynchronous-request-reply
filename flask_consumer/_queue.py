from abc import ABCMeta, abstractmethod


class AbstractQueue(metaclass=ABCMeta):
    """Abstract Base class for Queue"""

    def __init__(self):
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self) -> bool:
        """Is queue empty?"""
        return self._size == 0

    @abstractmethod
    def is_full(self) -> bool:
        """Is queue full?"""
        pass

    @abstractmethod
    def enqueue(self, value: str) -> None:
        """Insert element in queue."""
        pass

    @abstractmethod
    def dequeue(self):
        """Remove element from queue."""
        pass

    @abstractmethod
    def __iter__(self):
        pass


class QueueManager(AbstractQueue):
    """Queue implementation for job execution as
    "First Come First Serve".
    """

    def __init__(self, capacity=20):
        super().__init__()
        self._queue = [None for _ in range(capacity)]
        self._front, self._rear = 0, 0

    @property
    def queue(self) -> list:
        """Property to get queued elements."""
        return self._queue

    def __iter__(self):
        index = self._front
        while True:
            if index == self._rear:
                return
            yield self._queue[index]
            index += 1

    def enqueue(self, message_token: str) -> None:
        """
        Insert element in queue.

        :param message_token: `message_token`
        :type message_token: str
        :return:
        :rtype:
        """
        if self.is_full():
            self._expand()
        self._queue[self._rear] = message_token
        self._rear += 1
        self._size += 1

    def dequeue(self) -> str:
        """
        Remove element from queue.

        :return: 'message_token`
        :rtype: str
        """
        if self.is_empty():
            raise IndexError('Queue is empty!')
        message_token = self._queue[self._front]
        self._queue[self._front] = None
        self._front += 1
        self._size -= 1
        return message_token

    def _expand(self) -> None:
        """
        Expand size of queue.
        :return:
        :rtype:
        """
        self._queue += [None for _ in range(len(self._queue))]

    def is_full(self) -> bool:
        """
        Is queue full?

        :return: True or False
        :rtype: bool
        """
        return len(self._queue) == self._rear
