import utime
from misc import Power
from usr.quecframe.watchdog import WatchDog
from usr.quecframe.threading import Thread


wd = WatchDog()
wd.start()


def fun1():
    for i in range(10):
        print('fun1 feed...')
        wd.feed('fun1')
        utime.sleep(5)


def fun1_dump_callback():
    print('fun1 dump callback, restart now')
    Power.powerRestart()


if __name__ == '__main__':
    t1 = Thread(target=fun1)
    wd.register('fun1', callback=fun1_dump_callback)
    t1.start()
