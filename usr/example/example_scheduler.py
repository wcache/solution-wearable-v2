from usr.quecframe.scheduler import Scheduler
from usr.quecframe.datetime import DateTime, TimeDelta, TimeZone


scheduler = Scheduler()


# @scheduler.task(title='test1', interval=25,
#                 start_time=DateTime(2024, 1, 11, 13, 11),
#                 end_time=DateTime(2024, 1, 11, 13, 21))
def test1(*args, **kwargs):
    print('test1 function run: {}, {}, at: {}'.format(args, kwargs, DateTime.now()))


# @scheduler.task(datetime=DateTime(2024, 1, 10, 2, 58, 41, tz=UTC))
# @scheduler.task(datetime=DateTime.now() + TimeDelta(seconds=30))
# @scheduler.task(datetime=DateTime.utcnow() + TimeDelta(seconds=30))
# @scheduler.task(title='test2', datetime=DateTime.utcnow().astimezone(TimeZone(offset=8)) + TimeDelta(days=25))
def test2(*args, **kwargs):
    print('test2 function run: {}, {} at: {}'.format(args, kwargs, DateTime.now()))


# @scheduler.task(title='test3', interval=20)
def test3(*args, **kwargs):
    print('test3 function run: {}, {} at: {}'.format(args, kwargs, DateTime.now()))


@scheduler.task(title='test4', cron=(13, 39))
def test4(*args, **kwargs):
    print("alarm clock ... at: {}".format(DateTime.now()))


if __name__ == '__main__':
    scheduler.start()
    # scheduler.update(test3, interval=50)
    # print(test3.trigger.next_run_time)
    # scheduler.cancel(test3)
