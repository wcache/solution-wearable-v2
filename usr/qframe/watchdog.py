import utime
from .threading import Thread, Lock, Event, AsyncTask


class WatchDog(object):
    INTERVAL = 10

    def __init__(self):
        self.register_map = {}
        self.lock = Lock()
        self.listen_thread = Thread(target=self.__listen_thread_worker)

    def start(self):
        self.listen_thread.start()

    def register(self, infname, callback=None):
        with self.lock:
            if infname in self.register_map:
                raise ValueError
            self.register_map[infname] = (Event(), callback)

    def cancel(self, infname):
        with self.lock:
            self.register_map.pop(infname, None)

    def feed(self, infname):
        self.register_map[infname][0].set()

    def __listen_thread_worker(self):
        while True:
            for infname, value in self.register_map.items():
                e, cb = value
                if not e.is_set():
                    AsyncTask(target=cb).delay()
                else:
                    e.clear()
            utime.sleep(self.INTERVAL)

    @classmethod
    def set_interval(cls, seconds):
        if not isinstance(seconds, int):
            raise TypeError('`seconds must be int`')
        cls.INTERVAL = seconds
