import usocket
from .logging import getLogger
from .threading import Thread


logger = getLogger(__name__)


class UDPConnection(object):
    SOCKET_TYPE = usocket.SOCK_DGRAM
    DEFAULT_TIMEOUT = 10

    class TimeoutError(Exception):
        pass

    class UnboundError(Exception):
        pass

    def __init__(self, addr, timeout=None, keep_alive=None):
        self.host, self.port = addr
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.__keep_alive = keep_alive
        self.__sock = None

    def __repr__(self):
        return '{}(({},{}))'.format(type(self).__name__, repr(self.host), repr(self.port))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args, **kwargs):
        self.disconnect()

    def __getaddrinfo(self):
        rv = usocket.getaddrinfo(self.host, self.port)
        if not rv:
            raise ValueError('DNS detect error')
        family = rv[0][0]
        ip, port = rv[0][4]
        return family, ip, port

    def connect(self):
        family, ip, port = self.__getaddrinfo()
        self.__sock = usocket.socket(family, self.SOCKET_TYPE)
        self.__sock.connect((ip, port))
        if self.timeout >= 0:
            self.__sock.settimeout(self.timeout)
        if self.__keep_alive and self.__keep_alive > 0:
            self.__sock.setsockopt(usocket.SOL_SOCKET, usocket.TCP_KEEPALIVE, self.__keep_alive)

    def disconnect(self):
        if self.__sock:
            self.__sock.close()
            self.__sock = None

    @property
    def sock(self):
        if self.__sock is None:
            raise self.UnboundError('socket unbound! you need to connect it first!')
        return self.__sock

    def write(self, data):
        return self.sock.send(data) == len(data)

    def read(self, size=1024):
        try:
            return self.sock.recv(size)
        except Exception as e:
            if isinstance(e, OSError) and e.args[0] == 110:
                raise self.TimeoutError(str(self))  # read timeout.
            else:
                raise e


class TCPConnection(UDPConnection):
    SOCKET_TYPE = usocket.SOCK_STREAM

    def get_status_code(self):
        try:
            return self.sock.getsocketsta()
        except self.UnboundError:
            return 99


class IOBufferReader(object):

    def __init__(self, conn, read_callback, read_size=1024):
        assert hasattr(conn, 'read'), 'connection object has no read method'
        assert callable(read_callback), 'read_callback not callable'
        self.__read_thread = None
        self.__read_size = read_size
        self.__read_callback = read_callback
        self.conn = conn

    def start(self):
        self.__read_thread = Thread(target=self.__read_thread_worker)
        self.__read_thread.start()

    def stop(self):
        if self.__read_thread:
            self.__read_thread.terminate()
            self.__read_thread = None

    def __recv_callback(self, data):
        try:
            self.__read_callback(data)
        except Exception as e:
            logger.error('{} recv_callback error: {}'.format(self.conn, e))

    def __read_thread_worker(self):
        while True:
            try:
                data = self.conn.read(self.__read_size)
            except self.conn.TimeoutError:
                # logger.debug('{} read timeout'.format(self.conn))
                self.__recv_callback(None)
                continue
            except Exception as e:
                logger.error('{} read error: {}; recv thread broken'.format(self.conn, e))
                break
            else:
                if not data:  # when tcp closed by peer, a b'' received and we just break out
                    break
                self.__recv_callback(data)


class UDPClient(object):
    connection_class = UDPConnection
    buffer_size = 1024
    read_timeout = 10

    def __init__(self, addr, timeout=None, keep_alive=None):
        self.__conn = self.connection_class(addr, self.read_timeout if timeout is None else timeout, keep_alive)
        self.write = self.__conn.write
        self.read = self.__conn.read
        self.__reader = IOBufferReader(self.__conn, self.recv_callback, read_size=self.buffer_size)

    @property
    def conn(self):
        return self.__conn

    def connect(self):
        logger.info('{} connect'.format(self.__conn))
        try:
            self.__conn.connect()
        except Exception as e:
            logger.error('{} connect failed: {}'.format(self.__conn, e))
            return False
        self.__reader.start()
        return True

    def disconnect(self):
        logger.info('{} disconnect'.format(self.__conn))
        try:
            self.__reader.stop()
            self.__conn.disconnect()
        except Exception as e:
            logger.error('{} disconnect failed: {}'.format(self.__conn, e))
            return False
        return True

    def recv_callback(self, data):
        raise NotImplementedError('you must implement this method')


class TCPClient(UDPClient):
    connection_class = TCPConnection
