
class Singleton(object):

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance

    def __repr__(self):
        return repr(self.cls)


class _Node(object):

    def __init__(self, data, next_=None, prev=None):
        self.data = data
        self.next = next_
        self.prev = prev

    def __repr__(self):
        return '{}(data={})'.format(type(self).__name__, self.data)


class DoubleLinkList(object):

    def __init__(self):
        self.__root = _Node(None)
        self.__root.next = self.__root
        self.__root.prev = self.__root

    def __iter__(self):
        curr = self.__root.next
        while curr != self.__root:
            yield curr
            curr = curr.next

    def __len__(self):
        result = 0
        for _ in self:
            result += 1
        return result

    def is_empty(self):
        return self.__root.next is None

    def add(self, data):
        """头插"""
        node = _Node(data, next_=self.__root.next, prev=self.__root)
        self.__root.next.prev = node
        self.__root.next = node
        return node

    def append(self, data):
        """尾插"""
        node = _Node(data, next_=self.__root, prev=self.__root.prev)
        self.__root.prev.next = node
        self.__root.prev = node
        return node

    def insert(self, data1, data2):
        """指定位置插入（将data2插入data1前）

        :param data1: 节点数据域元素
        :param data2: 节点数据域元素
        :return: data所属节点_Node
        """
        pos = self.search(data1)
        if pos is None:
            raise ValueError('{} not in list'.format(data1))
        node = _Node(data2, next_=pos, prev=pos.prev)
        pos.prev.next = node
        pos.prev = node
        return node

    def search(self, data):
        """查找data所属节点，data的类型必须实现__eq__

        :param data: 链表节点数据域元素
        :return: _Node节点 或 None
        """
        for node in self:
            if node.data == data:
                return node

    def remove(self, data):
        """删除data所属节点

        :param data: 链表节点数据域元素
        :return: None
        :raise: 元素节点不存在抛ValueError
        """
        node = self.search(data)
        if node is None:
            raise ValueError('{} not in link'.format(data))
        node.prev.next = node.next
        node.next.prev = node.prev


class OrderedDict(object):

    def __init__(self, iterable=None):
        self.__keys_link = DoubleLinkList()
        self.__key_node_map = {}
        self.__storage = {}
        if isinstance(iterable, (tuple, list)):
            self.__load(iterable)

    def __load(self, sequence):
        for k, v in sequence:
            self[k] = v

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, [(k, v) for k, v in self.items()])

    def __iter__(self):
        return (node.data for node in self.__keys_link)

    def __setitem__(self, key, value):
        if key not in self.__storage:
            self.__key_node_map[key] = self.__keys_link.append(key)
        self.__storage[key] = value

    def __getitem__(self, item):
        return self.__storage[item]

    def __delitem__(self, key):
        del self.__storage[key]
        node = self.__key_node_map.pop(key)
        node.prev.next = node.next
        node.next.prev = node.prev

    def keys(self):
        return iter(self)

    def values(self):
        return (self.__storage[key] for key in self)

    def items(self):
        return ((k, self.__storage[k]) for k in self)

    def get(self, key, default=None):
        if key not in self.__storage:
            return default
        return self.__storage[key]

    def pop(self, key, default=None):
        if key not in self.__storage:
            return default
        temp = self[key]
        del self[key]
        return temp

    def update(self, obj):
        for k, v in obj.items():
            self[k] = v

    def setdefault(self, key, value):
        if key in self.__storage:
            return self[key]
        else:
            self[key] = value
            return value


class Int(object):
    """serialize signed/unsigned Integer to/from bytes"""

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    def to_bytes(self, length=1, byteorder='big', signed=False):
        if byteorder == 'little':
            order = range(length)
        elif byteorder == 'big':
            order = reversed(range(length))
        else:
            raise ValueError("byteorder must be either 'little' or 'big'")
        return bytes((self.value >> i * 8) & 0xff for i in order)

    @classmethod
    def from_bytes(cls, raw, byteorder='big', signed=False):
        if byteorder == 'little':
            little_ordered = list(raw)
        elif byteorder == 'big':
            little_ordered = list(reversed(raw))
        else:
            raise ValueError("byteorder must be either 'little' or 'big'")
        n = sum(b << i * 8 for i, b in enumerate(little_ordered))
        if signed and little_ordered and (little_ordered[-1] & 0x80):
            n -= 1 << 8 * len(little_ordered)
        return n
