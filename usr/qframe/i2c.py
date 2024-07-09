from machine import I2C


class I2CInterface(object):

    class I2CReadError(Exception):
        pass

    class I2CWriteError(Exception):
        pass

    def __init__(self, i2c, slaveaddr):
        if not isinstance(i2c, I2C):
            raise TypeError('`i2c` should be machine.I2C type')
        self.__i2c = i2c
        self.__slaveaddr = slaveaddr

    def read(self, addr, size=1, delay=0):
        """读寄存器

        :param addr: I2C 寄存器地址（bytes or bytearray）。
        :param size: 读取的字节长度。
        :param delay: 延时，数据转换缓冲时间(单位ms)，int类型。
        :return:
        """
        if size <= 0:
            raise ValueError('`size` should be greater than 0')
        data = bytearray(size)
        if self.__i2c.read(self.__slaveaddr, addr, len(addr), data, size, delay) != 0:
            raise self.I2CReadError("slave 0x{:X} read failed".format(self.__slaveaddr))
        return data

    def write(self, addr, data):
        """写寄存器

        :param addr: I2C 寄存器地址（bytes or bytearray）。
        :param data: 写入的数据，bytearray or bytes类型
        :return:
        """
        if not isinstance(data, (bytearray, bytes)):
            raise TypeError('`data` should be bytearray or bytes')
        if self.__i2c.write(self.__slaveaddr, addr, len(addr), data, len(data)) != 0:
            raise self.I2CWriteError("slave 0x{:X} write failed".format(self.__slaveaddr))
