import uzlib
from .pathlib import Path


class TarInfo(object):

    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        if not hasattr(self, '__file_name__'):
            setattr(self, '__file_name__', self.data[:100].rstrip(b'\x00').decode())
        return getattr(self, '__file_name__')

    @property
    def size(self):
        if not hasattr(self, '__size__'):
            setattr(self, '__size__', int(self.data[124:135], 8))
        return getattr(self, '__size__')

    @property
    def typeflag(self):
        if not hasattr(self, '__typeflag__'):
            setattr(self, '__typeflag__', self.data[156:157].decode())
        return getattr(self, '__typeflag__')

    def is_dir(self):
        return self.typeflag == '5'

    def is_file(self):
        return self.typeflag == '0'


class TarFile(object):
    BLOCK_SIZE = 512

    def __init__(self, name):
        self.name = name
        self.update_file_list = []
        self.fp = open(self.name, 'rb')
        self.fp.seek(10)
        self.file = uzlib.DecompIO(self.fp, -15, 1)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.fp.close()

    @classmethod
    def open(cls, name):
        return cls(name)

    def close(self):
        self.fp.close()

    def read_block(self):
        return self.file.read(self.BLOCK_SIZE)

    def __file_process(self, tarinfo, parent_dir):
        if not tarinfo.name:
            # invalid block
            return
        target_path = Path(parent_dir) / Path(tarinfo.name)
        # print('file_path: {}; target_path: {}; size: {}'.format(tarinfo.name, str(target_path), tarinfo.size))
        if tarinfo.is_file():
            # record update files
            self.update_file_list.append({"file_path": tarinfo.name, "size": tarinfo.size})
            # mkdir parent dir
            if not target_path.parent.exists():
                target_path.parent.mkdir()
            # touch file
            with target_path.open("wb") as update_file:
                total_blocks = tarinfo.size // self.BLOCK_SIZE
                for i in range(total_blocks):
                    update_file.write(self.read_block())
                last_size = tarinfo.size % self.BLOCK_SIZE
                if last_size:
                    update_file.write(self.read_block()[:last_size])

    def extractall(self, path='/usr/'):
        if not path.startswith('/usr/'):
            raise ValueError('path must starts with "/usr/"')
        while True:
            data = self.read_block()
            if not data:
                break
            self.__file_process(TarInfo(data), parent_dir=path)
