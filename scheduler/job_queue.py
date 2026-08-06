"""
Experiment Queue
"""

from collections import deque


class JobQueue:

    def __init__(self):

        self._queue = deque()

    ############################################################

    def push(self, job):

        self._queue.append(job)

    ############################################################

    def pop(self):

        if self.empty():

            return None

        return self._queue.popleft()

    ############################################################

    def empty(self):

        return len(self._queue) == 0

    ############################################################

    def size(self):

        return len(self._queue)
