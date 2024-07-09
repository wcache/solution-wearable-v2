

class TarInfo(object):

    def __init__(self, name, size):
        self.name = ''  # 100
        self.mode = ''  # 8
        self.uid = ''  # 8
        self.gid = ''  # 8
        self.size = ''  # 12
        self.mtime = ''  # 12
        self.checksum = ''  # 8
        self.typeflag = ''  # 1
        self.linkname = ''  # 100
        self.magic = ''  # 6
        self.version = ''  # 2
        self.uname = ''  # 32
        self.gname = ''  # 32
        self.devmajor = ''  # 8
        self.devminor = ''  # 8
        self.prefix = ''  # 155
        self.padding = ''  # 12

    @classmethod
    def from_bytes(cls, data):
        return cls(
            data[:100].strip(b'\x00').decode(),
            data[124:136]
        )

    def to_bytes(self):
        pass


if __name__ == '__main__':
    with open('code.tar', 'rb') as f:
        raw = f.read(512)
        tarinfo = TarInfo.from_bytes(raw)
        print('name: {}; size: {}'.format(tarinfo.name, tarinfo.size))
