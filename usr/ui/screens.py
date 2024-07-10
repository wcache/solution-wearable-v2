"""表盘"""
import lvgl as lv
from usr.qframe.collections import Singleton, OrderedDict
from usr.qframe.logging import getLogger
from .widgets import Widget, Label, TileView, Image, Line
from .core import Style


logger = getLogger(__name__)


normal_style = Style(
    border_width=0,
    pad_all=0,
    outline_width=0,
    text_color=lv.color_white(),
    radius=0,
    bg_color=lv.color_black()
)


# 外挂字体库
arial18_style = Style(text_font_v2=('arial18.bin', 18, 0))
arial27_style = Style(text_font_v2=('arial27.bin', 27, 0))
arial55_style = Style(text_font_v2=('arial55.bin', 55, 0))


WEEKDAY_MAP = {
    0: '周日',
    1: '周一',
    2: '周二',
    3: '周三',
    4: '周四',
    5: '周五',
    6: '周六',
}


@Singleton
class MainTileView(TileView):

    def __init__(self):
        super().__init__(None)
        self.remove_style(None, lv.PART.SCROLLBAR)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.tile00 = self.add_tile(0, 0, lv.DIR.RIGHT)
        self.dial_plate = DialPlateScreen(self.tile00)

        self.tile10 = self.add_tile(1, 0, lv.DIR.LEFT | lv.DIR.RIGHT)
        self.watch = WatchFaceScreen(self.tile10)

        self.tile20 = self.add_tile(2, 0, lv.DIR.LEFT | lv.DIR.RIGHT)
        self.app_grid = AppGridScreen(self.tile20)

        self.tile30 = self.add_tile(3, 0, lv.DIR.LEFT | lv.DIR.RIGHT)
        self.app_list = AppListScreen(self.tile30)


class StatusBar(Widget):
    SIGNAL_ICON_SRC = 'E:/media/s4.png'
    BATTERY_ICON_SRC = 'E:/media/bat4.png'
    LOCATION_ICON_SRC = 'E:/media/point.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.END, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_pad_all=(5, lv.PART.MAIN | lv.STATE.DEFAULT),
            size=(lv.pct(100), lv.pct(10))
        )
        self.signal = Image(self, src=self.SIGNAL_ICON_SRC, align=lv.ALIGN.LEFT_MID)
        self.signal.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
        self.signal_text = Label(self, text='中国移动')
        self.signal_text.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
        self.signal_text.align_to(self.signal, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.signal_text.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        # {<symbol_id>: <symbol lvgl object>}
        self.symbol_dict = OrderedDict(  # keep in order
            (
                ('location', Image(self, src=self.LOCATION_ICON_SRC)),
                ('battery', Image(self, src=self.BATTERY_ICON_SRC))
            )
        )

    def hidden_symbol(self, name):
        self.symbol_dict[name].hidden()

    def show_symbol(self, name):
        self.symbol_dict[name].show()


@Singleton
class DialPlateScreen(Widget):
    BG_IMG_SRC = 'E:/media/20230913100558.png'
    H_IMG_FORMAT = 'E:/media/h{}.png'
    M_IMG_FORMAT = 'E:/media/m{}.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            size=(240, 280),
            style_bg_img_src=(self.BG_IMG_SRC, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.status_bar = StatusBar(self)

        self.layout1 = Widget(self, size=(116, 200), align=lv.ALIGN.LEFT_MID)
        self.layout1.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.hour_high = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=0, y=0)
        self.hour_low = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=58, y=0)
        self.minute_high = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=0, y=100)
        self.minute_low = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=58, y=100)

        self.date = Label(self, text='{:02d}/{:02d}'.format(0, 0))
        self.date.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.date.align_to(self.layout1, lv.ALIGN.OUT_RIGHT_TOP, 10, 0)

        self.weekday = Label(self, text=WEEKDAY_MAP[0])
        self.weekday.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weekday.align_to(self.date, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

    def set_datetime(self, month, day, hour, minute, weekday):
        self.date.set_text('{:02d}/{:02d}'.format(month, day))
        self.weekday.set_text(WEEKDAY_MAP[weekday])
        hour_string = '{:02d}'.format(hour)
        minute_string = '{:02d}'.format(minute)
        self.hour_high.set_src(self.H_IMG_FORMAT.format(hour_string[0]))
        self.hour_low.set_src(self.H_IMG_FORMAT.format(hour_string[1]))
        self.minute_high.set_src(self.H_IMG_FORMAT.format(minute_string[0]))
        self.minute_low.set_src(self.H_IMG_FORMAT.format(minute_string[1]))


@Singleton
class WatchFaceScreen(Widget):
    R_BG_IMG_SRC = 'E:/media/r-b.png'
    R_H_BG_IMG_SRC = 'E:/media/r-h.png'
    R_M_BG_IMG_SRC = 'E:/media/r-m.png'
    R_S_BG_IMG_SRC = 'E:/media/r-s.png'
    R_P_BG_IMG_SRC = 'E:/media/r-p.png'
    M_IMG_FORMAT = 'E:/media/m{}.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            size=(240, 280),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.status_bar = StatusBar(self)
        self.bg = Image(self, src=self.R_BG_IMG_SRC, x=5, y=50)
        # 原点
        self.point = Image(self.bg, src=self.R_P_BG_IMG_SRC, align=lv.ALIGN.CENTER)
        # 时针
        self.hour_hand = Image(self.bg, src=self.R_H_BG_IMG_SRC)
        self.hour_hand.align_to(self.point, lv.ALIGN.OUT_TOP_MID, 0, 12)
        self.hour_hand.set_pivot(6, 46)
        # 分针
        self.minute_hand = Image(self.bg, src=self.R_M_BG_IMG_SRC)
        self.minute_hand.align_to(self.point, lv.ALIGN.OUT_TOP_MID, 0, 12)
        self.minute_hand.set_pivot(15, 109)
        # 秒针
        self.second_hand = Image(self.bg, src=self.R_S_BG_IMG_SRC)
        self.second_hand.align_to(self.point, lv.ALIGN.OUT_TOP_MID, 0, 19)
        self.second_hand.set_pivot(7, 106)

        self.layout1 = Widget(self.bg, size=(116, 120), align=lv.ALIGN.CENTER)
        self.layout1.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.layout1.move_background()
        self.hour_high = Image(self.layout1, src=self.M_IMG_FORMAT.format(0), x=0, y=0)
        self.hour_low = Image(self.layout1, src=self.M_IMG_FORMAT.format(0), x=58, y=0)
        self.date = Label(self.layout1, text='{:02d}/{:02d}'.format(0, 0), align=lv.ALIGN.BOTTOM_LEFT)
        self.date.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weekday = Label(self.layout1, text=WEEKDAY_MAP[0], align=lv.ALIGN.BOTTOM_RIGHT)
        self.weekday.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)

    def update(self, month, day, hour, minute, second, weekday):
        angle_for_second = second * 6  # 秒度
        self.second_hand.set_angle(angle_for_second * 10)
        angle_for_minute = minute * 6 + angle_for_second / 60  # 分度
        self.minute_hand.set_angle(int(angle_for_minute * 10))
        angle_for_hour = hour * 30 + angle_for_minute / 12  # 时度
        self.hour_hand.set_angle(int(angle_for_hour * 10))
        self.date.set_text('{:02d}/{:02d}'.format(month, day))
        self.weekday.set_text(WEEKDAY_MAP[weekday])


@Singleton
class SleepModeScreen(Widget):
    NOTICE_ICON_SRC = 'E:/media/bell-03.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            size=(240, 280),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.time = Label(self, text='{:02d}:{:02d}'.format(0, 0), align=lv.ALIGN.CENTER, y=-50)
        self.time.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.date = Label(self, text='{:02d}月{:02d}日'.format(0, 0))
        self.date.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.date.align_to(self.time, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 0)

        self.weekday = Label(self, text=WEEKDAY_MAP[0])
        self.weekday.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weekday.align_to(self.time, lv.ALIGN.OUT_BOTTOM_RIGHT, 0, 0)

        self.notice = Widget(
            self,
            size=(130, 30),
            style_border_width=(1, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_border_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_outline_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(20, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.notice.align_to(self.time, lv.ALIGN.BOTTOM_MID, 0, 60)
        self.notice_img = Image(self.notice, src=self.NOTICE_ICON_SRC, align=lv.ALIGN.LEFT_MID, x=10)
        self.notice_text = Label(self.notice, text='暂无通知', align=lv.ALIGN.CENTER)
        self.notice_text.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.notice_text.align_to(self.notice_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)

    def set_datetime(self, month, day, hour, minute, weekday):
        self.time.set_text('{:02d}:{:02d}'.format(hour, minute))
        self.date.set_text='{:02d}月{:02d}日'.format(month, day)
        self.weekday.set_text(WEEKDAY_MAP[weekday])

    def set_notice_text(self, text):
        self.notice_text.set_text(text)


@Singleton
class AppGridScreen(Widget):
    HR_IMG_SRC = 'E:/media/app_heart.png'
    PHONE_IMG_SRC = 'E:/media/app_phone.png'
    TIMER_IMG_SRC = 'E:/media/app_time.png'
    WECHAT_IMG_SRC = 'E:/media/app_chat.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            size=(240, 280),
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW_WRAP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.hr = Image(self, src=self.HR_IMG_SRC)
        self.phone = Image(self, src=self.PHONE_IMG_SRC)
        self.timer = Image(self, src=self.TIMER_IMG_SRC)
        self.wechat = Image(self, src=self.WECHAT_IMG_SRC)


class ListItemBox(Widget):

    def __init__(self, parent, icon='', text=''):
        super().__init__(parent, size=(lv.pct(100), lv.pct(20)), style_bg_opa=(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT))
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.icon = Image(self, src=icon)
        self.icon.align(lv.ALIGN.LEFT_MID, 10, 0)
        self.text = Label(self, text=text)
        self.text.align_to(self.icon, lv.ALIGN.OUT_RIGHT_MID, 15, 0)
        self.text.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)


@Singleton
class AppListScreen(Widget):
    HR_IMG_SRC = 'E:/media/img_relation.png'
    PHONE_IMG_SRC = 'E:/media/img_notify.png'
    WECHAT_IMG_SRC = 'E:/media/img_message_small.png'
    TIMER_IMG_SRC = 'E:/media/img_alarm.png'

    def __init__(self, parent=None):
        super().__init__(
            parent,
            size=(240, 280),
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.COLUMN, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.hr = ListItemBox(self, icon=self.HR_IMG_SRC, text='心率')
        self.hr.add_event_cb(self.hr_event_clicked_cb, lv.EVENT.CLICKED, None)

        self.phone = ListItemBox(self, icon=self.PHONE_IMG_SRC, text='电话')
        self.phone.add_event_cb(self.phone_event_clicked_cb, lv.EVENT.CLICKED, None)

        self.wechat = ListItemBox(self, icon=self.WECHAT_IMG_SRC, text='微聊')
        self.wechat.add_event_cb(self.wechat_event_clicked_cb, lv.EVENT.CLICKED, None)

        self.timer = ListItemBox(self, icon=self.TIMER_IMG_SRC, text='倒计时')
        self.timer.add_event_cb(self.timer_event_clicked_cb, lv.EVENT.CLICKED, None)

    def hr_event_clicked_cb(self, event):
        pass

    def phone_event_clicked_cb(self, event):
        pass

    def wechat_event_clicked_cb(self, event):
        pass

    def timer_event_clicked_cb(self, event):
        pass


class Chart(Widget):
    
    def __init__(self, parent, bottom_text, top_text, color):
        super().__init__(
            parent,
            size=(240, 120),
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.seps = []
        self.sep_labels = []
        for i in range(5):
            line = Line(
                self,
                style_line_width=(1, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_rounded=(False, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_color=(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
            )
            line.set_points(
                [
                    {
                        "x": 55 * i,
                        "y": 0
                    },
                    {
                        "x": 55 * i,
                        "y": 100
                    },
                ],
                2
            )
            if i <= 3:
                label = Label(
                    self,
                    text=str(i * 6),
                    x=55 * i + 2,
                    y=85,
                    style_text_color=(color, lv.PART.MAIN | lv.STATE.DEFAULT)
                )
                self.sep_labels.append(label)
            else:
                label = Label(
                    self,
                    text=bottom_text,
                    x=55 * i - 30,
                    y=85,
                    style_text_color=(color, lv.PART.MAIN | lv.STATE.DEFAULT)
                )
                label2 = Label(
                    self,
                    text=top_text,
                    x=55 * i - 30,
                    y=0,
                    style_text_color=(color, lv.PART.MAIN | lv.STATE.DEFAULT)
                )
                self.sep_labels.append(label)
                self.sep_labels.append(label2)

            self.seps.append(line)

        self.lines = []
        for i in range(24):
            line = Line(
                self,
                style_line_width=(3, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_rounded=(True, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_color=(color, lv.PART.MAIN | lv.STATE.DEFAULT)
            )
            self.lines.append(line)

    def update(self, index, data):
        bottom, top = data  # 0~100
        self.lines[index].set_points(
            [
                {
                    "x": index * 10,
                    "y": 100 - bottom
                },
                {
                    "x": index * 10,
                    "y": 100 - top
                },
            ],
            2
        )


class MeasurementScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left-r.png'

    def __init__(self, parent=None, text='心率', color=lv.palette_main(lv.PALETTE.RED), bottom_text='85', top_text='100'):
        super().__init__(
            parent,
            size=(240, 280)
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_icon = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_title = Label(self, text=text)
        self.rt_title.set_style_text_color(color, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_title.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_title.align_to(self.rt_icon, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time_label = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.layout = Widget(
            self,
            size=(240, 250),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.COLUMN, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.START, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.START, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.START, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title = Label(self.layout, text=text)
        self.title.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value = Label(self.layout, text='96', style_text_color=(color, lv.PART.MAIN | lv.STATE.DEFAULT))
        self.value.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value_unit = Label(self.layout, text=('%' if self.measure_type in (0, 1) else '℃'))
        self.value_unit.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value_unit.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
        self.value_unit.align_to(self.value, lv.ALIGN.OUT_RIGHT_BOTTOM, 5, 0)
        self.text = Label(self.layout, text='98%, 10分钟前')
        self.text.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.set_style_text_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.chart = Chart(self.layout, bottom_text, top_text, color)


@Singleton
class HRMeasurementScreen(MeasurementScreen):
    measure_type = 0

    def __init__(self, parent=None):
        super().__init__(parent, text='心率', color=lv.palette_main(lv.PALETTE.RED), bottom_text='85', top_text='100')

        # for test
        self.chart.update(9, (47, 80))
        self.chart.update(10, (27, 80))
        self.chart.update(11, (17, 60))
        self.chart.update(12, (30, 70))
        self.chart.update(13, (40, 60))
        self.chart.update(14, (35, 70))
        self.chart.update(15, (27, 56))


@Singleton
class SPOMeasurementScreen(MeasurementScreen):
    measure_type = 1

    def __init__(self, parent=None):
        super().__init__(parent, text='血氧', color=lv.palette_main(lv.PALETTE.BLUE), bottom_text='85', top_text='100')

        # for test
        self.chart.update(9, (47, 80))
        self.chart.update(10, (27, 80))
        self.chart.update(11, (17, 60))
        self.chart.update(12, (30, 70))
        self.chart.update(13, (40, 60))
        self.chart.update(14, (35, 70))
        self.chart.update(15, (27, 56))


@Singleton
class TemperatureMeasurementScreen(MeasurementScreen):
    measure_type = 2

    def __init__(self, parent=None):
        super().__init__(parent, text='体温', color=lv.palette_main(lv.PALETTE.GREEN), bottom_text='35.4', top_text='41.0')

        # for test
        self.chart.update(9, (47, 80))
        self.chart.update(10, (27, 80))
        self.chart.update(11, (17, 60))
        self.chart.update(12, (30, 70))
        self.chart.update(13, (40, 60))
        self.chart.update(14, (35, 70))
        self.chart.update(15, (27, 56))
