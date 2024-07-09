import sms
from .threading import Queue, Thread
from .logging import getLogger


logger = getLogger(__name__)


class SmsClient(object):

    def __init__(self):
        self.__queue = Queue()
        self.__recv_thread = Thread(target=self.__recv_thread_worker)

    def __getattr__(self, name):
        return getattr(sms, name)

    def __put(self, args):
        # args[0]	整型	当前SIM卡卡槽的simId
        # args[1]	整型	短信索引
        # args[2]	字符串 短信存储位置
        self.__queue.put(args)

    def __recv_thread_worker(self):
        while True:
            args = self.__queue.get()
            index = args[1]
            try:
                data = self.searchTextMsg(index)
                if data != -1:
                    phone, msg, length = data
                    self.recv_callback(phone, msg)
                else:
                    logger.warn('get msg failed!')
            except Exception as e:
                logger.error('get msg error: {}'.format(e))
                continue
            finally:
                self.deleteMsg(index)

    def recv_callback(self, phone, msg):
        raise NotImplementedError
