from umqtt import MQTTClient as BaseMQTTConnection
from .logging import getLogger
from .threading import Thread


logger = getLogger(__name__)


class MQTTConnection(object):

    def __init__(self, *args, **kwargs):
        """init umqtt.MQTTClient instance.
        args:
            client_id - 客户端 ID，字符串类型，具有唯一性。
            server - 服务端地址，字符串类型，可以是 IP 或者域名。
        kwargs:
            port - 服务器端口（可选），整数类型，默认为1883，请注意，MQTT over SSL/TLS的默认端口是8883。
            user - （可选) 在服务器上注册的用户名，字符串类型。
            password - （可选) 在服务器上注册的密码，字符串类型。
            keepalive - （可选）客户端的keepalive超时值，整数类型，默认为0。
            ssl - （可选）是否使能 SSL/TLS 支持，布尔值类型。
            ssl_params - （可选）SSL/TLS 参数，字符串类型。
            reconn - （可选）控制是否使用内部重连的标志，布尔值类型，默认开启为True。
            version - （可选）选择使用mqtt版本，整数类型，version=3开启MQTTv3.1，默认version=4开启MQTTv3.1.1。
            clean_session - 布尔值类型，可选参数，一个决定客户端类型的布尔值。 如果为True，那么代理将在其断开连接时删除有关此客户端的所有信息。
                如果为False，则客户端是持久客户端，当客户端断开连接时，订阅信息和排队消息将被保留。默认为True。
            qos - MQTT消息服务质量（默认0，可选择0或1）.
                整数类型 0：发送者只发送一次消息，不进行重试 1：发送者最少发送一次消息，确保消息到达Broker。
        """
        self.args = args
        self.kwargs = kwargs
        self.clean_session = kwargs.pop('clean_session', True)
        self.__cli = None

    @property
    def cli(self):
        if self.__cli is None:
            raise ValueError('Mqtt Unbound error')
        return self.__cli

    def connect(self):
        self.__cli = BaseMQTTConnection(*self.args, **self.kwargs)
        self.__cli.set_callback(self.recv_callback)
        self.__cli.connect(clean_session=self.clean_session)

    def disconnect(self):
        if self.__cli is not None:
            self.__cli.disconnect()
            self.__cli = None

    def is_status_ok(self):
        return self.__cli is not None and self.__cli.get_mqttsta() == 0

    def publish(self, topic, msg, retain=False, qos=0):
        return self.cli.publish(topic, msg, retain=retain, qos=qos)

    def subscribe(self, topic, qos=0):
        self.cli.subscribe(topic, qos=qos)

    def recv_callback(self, topic, data):
        raise NotImplementedError('this method must be implemented!!!')


class MQTTClient(MQTTConnection):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__recv_thread = None

    def __recv_thread_worker(self):
        while True:
            try:
                self.cli.wait_msg()
            except Exception as e:
                logger.error('mqtt listen error: {}'.format(str(e)))
                break

    def __start_recv_thread(self):
        self.__recv_thread = Thread(target=self.__recv_thread_worker)
        self.__recv_thread.start()

    def __stop_recv_thread(self):
        self.__recv_thread.terminate()
        self.__recv_thread = None

    def disconnect(self):
        try:
            self.__stop_recv_thread()
            super().disconnect()
        except Exception as e:
            logger.error('mqtt disconnect failed: {}'.format(e))
            return False
        return True

    def connect(self):
        logger.info('mqtt connecting...')
        try:
            super().connect()
        except Exception as e:
            logger.error('mqtt connect failed. {}'.format(str(e)))
            return False
        logger.info('mqtt connect successfully.')
        self.__start_recv_thread()
        return True
