from usr.qframe.collections import OrderedDict
from usr.qframe.db import DataBase, IntField, TinyIntField, StringField, DateTimeField
from usr.qframe.datetime import DateTime


class ExampleInfo(DataBase):
    __dbpath__ = '/usr/example_info.db'
    __columns__ = OrderedDict(
        (
            ('id', IntField(default=0, signed=True)),
            ('age', TinyIntField(default=0)),
            ('name', StringField(10)),
            ('create_time', DateTimeField(default=lambda: DateTime.now()))
        )
    )

    __keys__ = ('create_time', )


def binary_search(
        intervals,
        target,
        start=0,
        end=None
):
    if end is None:
        end = len(intervals) - 1

    if start > end:
        return -1

    mid = (start + end) // 2
    interval = intervals[mid]

    if interval == target:
        return mid
    elif target < interval:
        return binary_search(intervals, target, start, mid - 1)
    else:
        return binary_search(intervals, target, mid + 1, end)