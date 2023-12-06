from threading import *

class myQueue:
    def __init__(self, size) -> None:
        self.storage = []
        self.storageLock = Lock()
        self.full = Semaphore(0)
        self.empty = Semaphore(size)

    def put(self, item):
        self.empty.acquire()
        self.storageLock.acquire()
        self.storage.append(item)
        self.storageLock.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.storageLock.acquire()
        item = self.storage.pop(0)
        self.storageLock.release()
        self.empty.release()
        return item