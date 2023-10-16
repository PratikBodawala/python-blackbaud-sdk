from multiprocessing import Queue
from threading import Thread

from requests import Session


class BlackBaudSession(Session):
    def __init__(self, subscription_key):
        super().__init__()
        self.headers.update({'Bb-Api-Subscription-Key': subscription_key})
        # self.input_queue = Queue()
        # self.output_queue = Queue()
        # self.worker = Thread(target=self._worker)
        # self.worker.start()

    # def _worker(self):
    #     while True:
    #         args, kwargs = self.input_queue.get()
    #         self.output_queue.put(super().request(*args, **kwargs))
    #
    # def request(
    #     self, *args, **kwargs
    # ):
    #     self.input_queue.put((args, kwargs))
    #     return self.output_queue.get()

    def __del__(self):
        # self.worker.join()
        self.close()
