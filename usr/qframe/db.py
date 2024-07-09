import ql_fs
from .datetime import DateTime
from .collections import OrderedDict, Int


class IntField(object):
    length = 4

    def __init__(self, default=None, byteorder='big', signed=False):
        self.default = default
        self.byteorder = byteorder
        self.signed = signed

    def to_bytes(self, value):
        return Int(value).to_bytes(self.length, byteorder=self.byteorder, signed=self.signed)

    def from_bytes(self, raw):
        return Int.from_bytes(raw, byteorder=self.byteorder, signed=self.signed)


class TinyIntField(IntField):
    length = 1


class SmallIntField(IntField):
    length = 2


class BigIntFiled(IntField):
    length = 8


class StringField(object):

    def __init__(self, length, default=None):
        self.length = length
        self.default = default

    def to_bytes(self, value):
        string_bytes = value.encode()
        string_bytes_length = len(string_bytes)
        if string_bytes_length <= self.length:
            return string_bytes + bytes([0] * (self.length - string_bytes_length))
        return string_bytes[:self.length]

    def from_bytes(self, raw):
        return raw.decode().strip(chr(0))


class DateTimeField(object):

    def __init__(self, default=None):
        self.length = 4
        self.default = default

    def to_bytes(self, value):
        return Int(value.timestamp).to_bytes(self.length, byteorder='big')

    def from_bytes(self, raw):
        return DateTime.fromtimestamp(Int.from_bytes(raw, byteorder='big'))


class DataBase(object):
    __db__ = bytearray()
    __dbpath__ = '/usr/database.db'
    __columns__ = OrderedDict()
    __keys__ = ()

    def __init__(self, **kwargs):
        for col, _type in self.__columns__.items():
            if col not in kwargs and _type.default is None:
                raise ValueError('\"{}\" is missing and no default value was found'.format(col))
            setattr(self, col, kwargs.get(col, _type.default() if callable(_type.default) else _type.default))

    def __str__(self):
        return '{}({})'.format(type(self).__name__, {k: getattr(self, k) for k in self.__columns__.keys()})

    @classmethod
    def __get_key_index(cls):
        key_index_list_map = getattr(cls, '__key_index_list_map__', None)
        if key_index_list_map is None:
            key_index_list_map = {key: [] for key in cls.__keys__}
            setattr(cls, '__key_index_list_map__', key_index_list_map)
        return key_index_list_map

    def __to_bytes(self):
        rv = bytearray()
        for k, _type in self.__columns__.items():
            rv.extend(_type.to_bytes(getattr(self, k)))
        return rv

    @classmethod
    def __from_bytes(cls, raw):
        index = 0
        rv = {}
        for k, _type in cls.__columns__.items():
            rv[k] = _type.from_bytes(raw[index: index + _type.length])
            index += _type.length
        return cls(**rv)

    def save(self):
        if self.offset is not None:
            for i, value in enumerate(self.__to_bytes()):
                self.__db__[self.offset + i] = value
        else:
            setattr(self, '__offset__', self.length())
            self.__db__.extend(self.__to_bytes())
        return self

    @classmethod
    def flush(cls, to_path=None):
        with open(to_path or cls.__dbpath__, 'wb') as f:
            f.write(cls.__db__)

    @classmethod
    def init(cls, from_path=None):
        if ql_fs.path_exists(from_path or cls.__dbpath__):
            with open(from_path or cls.__dbpath__, 'rb') as f:
                cls.__db__ = bytearray(f.read())

    @classmethod
    def length(cls):
        return len(cls.__db__)

    @classmethod
    def __block_size(cls):
        __block_size__ = getattr(cls, '__block_size__', None)
        if __block_size__ is None:
            __block_size__ = sum((_type.length for _type in cls.__columns__.values()))
            setattr(cls, '__block_size__', __block_size__)
        return __block_size__

    @property
    def offset(self):
        return getattr(self, '__offset__', None)

    @classmethod
    def all(cls):
        for i in range(0, cls.length(), cls.__block_size()):
            self = cls.__from_bytes(cls.__db__[i: i + cls.__block_size()])
            setattr(self, '__offset__', i)
            yield self

    @classmethod
    def get(cls, index):
        offset = index * cls.__block_size() if index >= 0 else (cls.length() + index * cls.__block_size())
        raw = cls.__db__[offset: offset + cls.__block_size()]
        if raw:
            self = cls.__from_bytes(raw)
            setattr(self, '__offset__', offset)
            return self

    @classmethod
    def slice(cls, start=None, end=None):
        start_offset = (start * cls.__block_size() if start >= 0 else (
                    cls.length() + start * cls.__block_size())) if start is not None else 0
        end_offset = (end * cls.__block_size() if end >= 0 else (
                    cls.length() + end * cls.__block_size())) if end is not None else cls.length()
        raw = cls.__db__[start_offset: end_offset]
        for i in range(0, len(raw), cls.__block_size()):
            self = cls.__from_bytes(raw[i: i + cls.__block_size()])
            setattr(self, '__offset__', start_offset + i)
            yield self
