from usr.business.tlv import HTlvC, Parser
from usr.quecframe.core.common import Serial


def make_request_message():

    print('模块主发测试报文: ')
    # >>>>>> 1. 语音拨号请求报文
    print('1.1 挂断电话: ', HTlvC(0x0001, value=b'\x00').to_hex().decode())
    print('1.2 拨打电话: ', HTlvC(0x0001, value=b'\x0118588269037').to_hex().decode())
    print('1.3 接听电话: ', HTlvC(0x0001, value=b'\x02').to_hex().decode())
    # <<<<<<

    # >>>>>> 2. 发短信请求报文
    print('2.1 发短信: ', HTlvC(0x0002, value=b'+8618588269037;hello world!').to_hex().decode())
    # <<<<<<

    # >>>>>> 3. 查询4G模块状态请求报文
    print('3.1 查询4G模块状态: ', HTlvC(0x0003).to_hex().decode())
    # <<<<<<

    # >>>>>> 4. 查询设备号是否绑卡请求报文
    print('4.1 查询设备号是否绑卡: ', HTlvC(0x0004, value=b'1343CF010171').to_hex().decode())
    # <<<<<<

    # >>>>>> 5. 手表请求打开摄像头扫描收款码请求报文
    print('5.1 手表请求打开摄像头扫描收款码: ', HTlvC(0x0005, value=b'1343CF010171').to_hex().decode())
    # <<<<<<

    # >>>>>> 6. 模块发起付款请求报文
    print(
        '6.1 模块发起付款: ',
        HTlvC(
            0x0006, value=b'\xe9\x9f\xa6\xe5\xb0\x91;1;fgfTtfRY4izFvoyXwU9W84zDgNGn44hfbVLY5J'
        ).to_hex().decode()
    )
    # <<<<<<


def test_HTlvC_server():
    serial = Serial()
    serial.open()
    parser = Parser()
    while True:
        try:
            data = serial.read(1024, timeout=10)
            # print('data: ', data)
        except serial.TimeoutError:
            parser.clear()
            continue
        parser.parse(data)
        for m in parser.messages:
            print('tlv msg: ', m)


if __name__ == '__main__':
    # Thread(target=test_HTlvC_server).start()
    make_request_message()
