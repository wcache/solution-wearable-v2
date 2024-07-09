import uos
import ql_fs


class PurePath(object):

    def __init__(self, path=None):
        if not isinstance(path, (str, list, tuple, type(None), type(self))):
            raise TypeError('path type must be in (str, list, tuple)')
        path = '/usr' if not path or path in ('.', './') else path
        self.__parts = self.__parse_parts(path)
        self.__path = self.__get_path_from_parts(self.__parts)

    def __repr__(self):
        return '{}(\"{}\")'.format(type(self).__name__, self.__path)

    def __str__(self):
        return self.__path

    def __truediv__(self, other):
        parts = self.parts + other.parts[1:] if other.parts[0] == '/' else self.parts + other.parts
        return type(self)(parts)

    @staticmethod
    def __get_path_from_parts(parts):
        if parts[0] == '/':
            return '/' + '/'.join(parts[1:])
        return '/'.join(parts)

    def __parse_parts(self, path):
        parts = []
        if isinstance(path, str):
            if path.startswith('/'):
                parts = ['/']
            parts.extend([_ for _ in path.split('/') if _ not in ('', '.')])
        elif isinstance(path, type(self)):
            parts = path.parts
        else:
            parts = path
        return parts

    @property
    def parts(self):
        return tuple(self.__parts)

    @property
    def name(self):
        if len(self.__parts) == 1 and self.__parts[0] == '/':
            return ''
        return self.__parts[-1]

    @property
    def suffix(self):
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[i:]
        else:
            return ''

    @property
    def stem(self):
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[:i]
        else:
            return name

    @property
    def parent(self):
        if len(self.__parts) == 1:
            return self
        return type(self)(self.__parts[:-1])

    def with_name(self, name):
        if not self.name:
            raise ValueError("{} has an empty name".format(self))
        return type(self)(self.__parts[:-1] + [name])

    def with_stem(self, stem):
        return self.with_name(stem + self.suffix)

    def with_suffix(self, suffix):
        if suffix and not suffix.startswith('.') or suffix == '.':
            raise ValueError("Invalid suffix {}".format(suffix))
        return self.with_name(self.stem + suffix)


class Path(PurePath):

    def open(self, mode='r'):
        return open(str(self), mode)

    @classmethod
    def getcwd(cls):
        return cls(uos.getcwd())

    @classmethod
    def chdir(cls, path):
        return uos.chdir(path)

    def iterdir(self):
        for item in uos.listdir(str(self)):
            yield self / Path(item)

    def touch(self, exist_ok=True):
        if exist_ok:
            fd = self.open(mode='w')
        else:
            if ql_fs.path_exists(str(self)):
                raise ValueError('{} existed, can not touch'.format(self))
            fd = self.open(mode='w')
        fd.close()

    def remove(self):
        return uos.remove(str(self))

    def mkdir(self):
        return ql_fs.mkdirs(str(self))

    def rmdir(self):
        return ql_fs.rmdirs(str(self))

    def rename(self, name):
        return uos.rename(str(self), name)

    def exists(self):
        return ql_fs.path_exists(str(self))

    def stat(self):
        return uos.stat(str(self))

    def is_dir(self):
        return self.stat()[0] == 0x4000

    def is_file(self):
        return self.stat()[0] == 0x8000
