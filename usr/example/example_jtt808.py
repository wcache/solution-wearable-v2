from usr.extensions.jtt808 import *


if __name__ == '__main__':
    JTT808Config.update(
        encryptmode=EncryptMode.NULL,
        version=1,
        phonenum=b'0123456789'
    )
    for m in JTT808MultiMsg(
            0x0900,
            bytes([0xff]) * 2096
    ).split():
        print('xx: ', m)

    print(ReportLocationMsg(b'123'))
