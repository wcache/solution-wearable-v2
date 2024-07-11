"""表盘"""
import lvgl as lv
from usr.qframe.collections import Singleton, OrderedDict
from usr.qframe.logging import getLogger
from .widgets import Widget, Label, TileView, Image, Line, Button, Roller, Arc, Switch
from .core import Style, Anim


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


class KeypadScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left.png'
    DEL_IMG_SRC = 'E:/media/delete.png'
    NUMBER_ICON_SRC_FORMAT = 'E:/media/b{}.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_icon = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)

        self.number_area = Widget(
            self,
            y=lv.pct(5),
            size=(lv.pct(80), lv.pct(15)),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_align=(lv.ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.number_area.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.number = Label(self.number_area, text='', style_align=(lv.ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT))
        self.number.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.real_number = ''

        self.delete_area = Widget(
            self,
            size=(lv.pct(20), lv.pct(15)),
            x=lv.pct(80),
            y=lv.pct(5),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.delete_area.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.delete = Image(
            self.delete_area,
            src=self.DEL_IMG_SRC,
            style_align=(lv.ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.delete_area.add_event_cb(self.delete_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.btn_layout = Widget(
            self,
            y=lv.pct(20),
            size=(lv.pct(100), lv.pct(80)),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.MAIN | lv.STATE.DEFAULT),
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW_WRAP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.btn_layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        for key in [str(x) for x in range(1, 10)]:
            btn = Button(
                self.btn_layout,
                size=(72, 44),
                style_bg_color=(lv.color_hex(0x48586F), lv.PART.MAIN | lv.STATE.DEFAULT)
            )
            btn.add_event_cb(self.btn_event_clicked_handler, lv.EVENT.CLICKED, None)
            btn.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
            btn.label.set_text(key)

        self.temp = Widget(self.btn_layout, size=(72, 44))
        self.temp.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        btn = Button(
            self.btn_layout,
            size=(72, 44),
            style_bg_color=(lv.color_hex(0x48586F), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        btn.add_event_cb(self.btn_event_clicked_handler, lv.EVENT.CLICKED, None)
        btn.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        btn.label.set_text('0')

        self.ok = Image(self.btn_layout, src=self.NUMBER_ICON_SRC_FORMAT.format(10))
        self.ok.add_flag(lv.obj.FLAG.CLICKABLE)
        self.ok.add_event_cb(self.ok_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.add_event_cb(self.event_screen_loaded_handler, 39, None)
        self.add_event_cb(self.event_screen_unloaded_handler, 40, None)

    def event_screen_loaded_handler(self, event):
        self.real_number = ''
        self.number.set_text('')

    def event_screen_unloaded_handler(self, event):
        self.del_async()

    def delete_event_clicked_handler(self, event):
        logger.debug('{} delete_event_clicked_handler'.format(type(self).__name__))
        self.real_number = self.real_number[:-1]
        string = self.real_number
        if len(string) > 14:
            string = '{:.>14s}'.format(string[-11:])
        self.number.set_text(string)

    def btn_event_clicked_handler(self, event):
        target = event.get_target()
        logger.debug('{} number_event_clicked_handler, number is: {}'.format(type(self).__name__, target.label.get_text()))
        self.real_number += str(target.label.get_text())
        string = self.real_number
        if len(string) > 14:
            string = '{:.>14s}'.format(string[-11:])
        self.number.set_text(string)

    def ok_event_clicked_handler(self, event):
        # TODO: 拨打电话
        logger.debug('{} ok_event_clicked_handler')


class VoiceCallScreen(Widget):
    CANCEL_ICON_SRC = 'E:/media/cancel.png'
    RECV_ICON_SRC = 'E:/media/receive.png'

    def __init__(self, parent=None, name='李琳', text='正在呼叫'):
        super().__init__(parent, size=(240, 280))
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.title = Label(self, text='电话', align=lv.ALIGN.TOP_LEFT)
        self.title.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.name = Label(self, text=name, align=lv.ALIGN.CENTER)
        self.name.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.text = Label(self, text=text)
        self.text.align_to(self.name, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        self.text.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.recv = Image(self, src=self.RECV_ICON_SRC)
        self.recv.align(lv.ALIGN.BOTTOM_RIGHT, -10, -10)
        self.recv.add_event_cb(self.recv_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.cancel = Image(self, src=self.CANCEL_ICON_SRC)
        self.cancel.align(lv.ALIGN.BOTTOM_LEFT, 10, -10)
        self.cancel.add_event_cb(self.cancel_event_clicked_handler, lv.EVENT.CLICKED, None)

    def recv_event_clicked_handler(self, event):
        pass

    def cancel_event_clicked_handler(self, event):
        pass


class StepChart(Widget):

    def __init__(self, parent):
        super().__init__(
            parent,
            size=(240, 130),
        )
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.bg_list = []
        self.lines = []
        for i in range(24):
            bg_line = Line(
                self,
                x=i * 5 + 2,
                y=5,
                style_line_width=(5, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_rounded=(True, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_color=(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
            )
            bg_line.move_background()
            bg_line.set_points(
                [
                    {
                        "x": i * 5 + 2,
                        "y": 0
                    },
                    {
                        "x": i * 5 + 2,
                        "y": 100
                    }
                ],
                2
            )
            self.bg_list.append(bg_line)

            line = Line(
                self,
                x=i * 5 + 2,
                y=5,
                style_line_width=(5, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_rounded=(True, lv.PART.MAIN | lv.STATE.DEFAULT),
                style_line_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT)
            )
            line.set_points(
                [
                    {
                        "x": i * 5 + 2,
                        "y": 50
                    },
                    {
                        "x": i * 5 + 2,
                        "y": 100
                    }
                ],
                2
            )
            self.lines.append(line)

        self.text1 = Label(self, text='0:00', align=lv.ALIGN.BOTTOM_LEFT)
        self.text2 = Label(self, text='12:00', align=lv.ALIGN.BOTTOM_MID)
        self.text3 = Label(self, text='24:00', align=lv.ALIGN.BOTTOM_RIGHT)

    def update(self, index, value):
        self.lines[index].set_points(
            [
                {
                    "x": index * 5 + 2,
                    "y": 100
                },
                {
                    "x": index * 5 + 2,
                    "y": 100 - value
                }
            ],
            2
        )


class StepScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left.png'

    def __init__(self, parent=None):
        super().__init__(parent, size=(240, 280))

        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_icon = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_title = Label(self, text='步数')
        self.rt_title.set_style_text_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT)
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
        self.title = Label(self.layout, text='总步数')
        self.title.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value = Label(self.layout, text='12345', style_text_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.value.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value_unit = Label(self.layout, text='步')
        self.value_unit.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.value_unit.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
        self.value_unit.align_to(self.value, lv.ALIGN.OUT_RIGHT_BOTTOM, 5, 0)
        self.text = Label(self.layout, text='建议每日行走8000步')
        self.text.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.set_style_text_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)

        self.chart = StepChart(self.layout)

        # for test
        import urandom
        for i in range(24):
            value = urandom.randint(10, 100)
            self.chart.update(i, value)


class StepSettingScreen(Widget):

    def __init__(self, parent=None):
        super().__init__(parent, size=(240, 320))
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.title = Label(self, text='取消', align=lv.ALIGN.TOP_LEFT)
        self.title.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.time = Label(self, text='10:09', align=lv.ALIGN.TOP_RIGHT)
        self.time.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.layout = Widget(
            self,
            size=(240, 250),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW_WRAP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text = Label(self.layout, text='目标设定')
        self.text.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.minus = Button(
            self.layout,
            text='-',
            size=(40, 40),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.minus.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.minus.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.minus.add_event_cb(self.minus_event_clicked_handler, lv.EVENT.CLICKED, None)
        self.target = Label(self.layout, text='8000')
        self.target.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.plus = Button(
            self.layout,
            text='+',
            size=(40, 40),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.plus.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.plus.add_event_cb(self.plus_event_clicked_handler, lv.EVENT.CLICKED, None)
        self.unit = Label(self.layout, text='步')
        self.unit.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.unit.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.ok = Button(self.layout, text='确定', size=(200, 50))
        self.ok.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.ok.set_style_text_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.add_event_cb(self.ok_event_clicked_handler, lv.EVENT.CLICKED, None)

    def plus_event_clicked_handler(self, event):
        value = int(self.target.get_text())
        value += 500
        self.target.set_text(str(value))

    def minus_event_clicked_handler(self, event):
        value = int(self.target.get_text())
        value -= 500
        self.target.set_text(str(value))

    def ok_event_clicked_handler(self, event):
        print('{} ok_event_clicked_handler'.format(type(self).__name__))


class CountDownSettingScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left-y.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_img = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_label = Label(self, text='设置', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.rt_label.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_label.align_to(self.rt_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.layout = Widget(
            self,
            size=(240, 250),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW_WRAP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.hours_label = Label(self.layout, text='小时', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.hours_label.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.minutes_label = Label(self.layout, text='分钟', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.minutes_label.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.seconds_label = Label(self.layout, text='秒', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.seconds_label.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.roller_hours = Roller(
            self.layout,
            options=("\n".join(['{:02d}'.format(hour) for hour in range(24)]), lv.roller.MODE.NORMAL),
            visible_row_count=3,
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.SELECTED | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.roller_hours.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.roller_hours.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_hours.add_style(arial55_style, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_hours.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_hours.set_style_text_opa(lv.OPA._80, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_hours.add_event_cb(
            lambda event: print('roller_hours VALUE_CHANGED'),
            lv.EVENT.VALUE_CHANGED,
            None
        )
        self.sep1 = Label(self.layout, text=':')
        self.sep1.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.roller_minutes = Roller(
            self.layout,
            options=("\n".join(['{:02d}'.format(hour) for hour in range(60)]), lv.roller.MODE.NORMAL),
            visible_row_count=3,
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.SELECTED | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.roller_minutes.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_minutes.add_style(arial55_style, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_minutes.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_minutes.set_style_text_opa(lv.OPA._80, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_minutes.add_event_cb(
            lambda event: print('roller_minutes VALUE_CHANGED'),
            lv.EVENT.VALUE_CHANGED,
            None
        )
        self.sep2 = Label(self.layout, text=':')
        self.sep2.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.roller_seconds = Roller(
            self.layout,
            options=("\n".join(['{:02d}'.format(hour) for hour in range(60)]), lv.roller.MODE.NORMAL),
            visible_row_count=3,
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.SELECTED | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.roller_seconds.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_seconds.add_style(arial55_style, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_seconds.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_seconds.set_style_text_opa(lv.OPA._80, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_seconds.add_event_cb(
            lambda event: print('roller_seconds VALUE_CHANGED'),
            lv.EVENT.VALUE_CHANGED,
            None
        )

        self.cancel = Button(self.layout, text='取消', size=(100, 50))
        self.cancel.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.cancel.set_style_text_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.add_event_cb(self.cancel_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.ok = Button(self.layout, text='开始', size=(100, 50))
        self.ok.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_text_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.add_event_cb(self.ok_event_clicked_handler, lv.EVENT.CLICKED, None)

    def cancel_event_clicked_handler(self, event):
        print('{} cancel_event_clicked_handler'.format(type(self).__name__))

    def ok_event_clicked_handler(self, event):
        print('{} ok_event_clicked_handler'.format(type(self).__name__))


class CountDownScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left-y.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_img = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_label = Label(self, text='倒计时', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.rt_label.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_label.align_to(self.rt_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.arc = Arc(
            self,
            size=(200, 200),
            range=(0, 1000),
            rotation=270,
            bg_angles=(0, 360),
            style_arc_color=(lv.palette_main(lv.PALETTE.ORANGE), lv.PART.INDICATOR | lv.STATE.DEFAULT)
        )
        self.arc.center()
        self.arc.remove_style(None, lv.PART.KNOB)
        self.arc.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.arc.set_value(1000)

        self.total = Label(self.arc, text='1分钟')
        self.total.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.total.align(lv.ALIGN.CENTER, 0, -40)
        self.remaining = Label(self.arc, text='01:00')
        self.remaining.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.remaining.align(lv.ALIGN.CENTER, 0, 0)

        self.cancel = Button(self, text='取消', size=(100, 50))
        self.cancel.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_align(lv.ALIGN.BOTTOM_LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_text_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cancel.add_event_cb(self.cancel_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.ok = Button(self, text='开始', size=(100, 50))
        self.ok.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_align(lv.ALIGN.BOTTOM_RIGHT, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_text_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_opa(lv.OPA._30, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.set_style_bg_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ok.add_event_cb(self.ok_event_clicked_handler, lv.EVENT.CLICKED, None)

        self.total_seconds = 60
        self.anim = None

    def cancel_event_clicked_handler(self, event):
        print('{} cancel_event_clicked_handler'.format(type(self).__name__))
        if self.anim:
            lv.anim_del_all()
            self.anim = None

    def ok_event_clicked_handler(self, event):
        print('{} ok_event_clicked_handler'.format(type(self).__name__))
        if self.anim:
            return
        self.anim = Anim(
            var=self.arc,
            values=(1000, 0),
            time=self.total_seconds * 1000,
            custom_exec_cb=self.anim_custom_exec_cb,
            ready_cb=self.anim_ready_cb
        )
        self.anim.start()

    def anim_custom_exec_cb(self, anim, value):
        self.arc.set_value(value)
        self.remaining.set_text('{:02d}:{:02d}'.format(int(value * 0.06) // 60, int(value * 0.06) % 60))

    def anim_ready_cb(self, anim):
        self.anim = None


class AlarmItem(Image):
    RECT_ICON_SRC = 'E:/media/rectangle_57.png'

    def __init__(self, parent):
        super().__init__(parent, src=self.RECT_ICON_SRC)
        self.time = Label(self, text='08:00', align=lv.ALIGN.TOP_LEFT)
        self.time.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.weekdays = Label(self, text='一二三四五六日', align=lv.ALIGN.BOTTOM_LEFT)
        self.weekdays.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.switch = Switch(self, align=lv.ALIGN.RIGHT_MID)
        self.switch.add_event_cb(self.switch_event_clicked_handler, lv.EVENT.VALUE_CHANGED, None)

    def switch_event_clicked_handler(self, event):
        print('{} switch_event_clicked_handler'.format(type(self).__name__))


class AlarmScreen(Widget):
    ADD_ICON_SRC = 'E:/media/add_clock.png'
    RT_ICON_SRC = 'E:/media/chevron-left-y.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_img = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_label = Label(self, text='闹钟', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.rt_label.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_label.align_to(self.rt_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.layout = Widget(
            self,
            size=(240, 200),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.COLUMN, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.a1 = AlarmItem(self.layout)
        self.a2 = AlarmItem(self.layout)

        self.add_icon = Image(self, src=self.ADD_ICON_SRC, align=lv.ALIGN.BOTTOM_MID)
        self.add_icon.add_flag(lv.obj.FLAG.CLICKABLE)
        self.add_icon.add_event_cb(self.add_event_clicked_handler, lv.EVENT.CLICKED, None)

    def add_event_clicked_handler(self, event):
        print('{} add_event_clicked_handler'.format(type(self).__name__))


class AlarmSettingScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left-y.png'
    BTN_ICON_SRC = 'E:/media/rectangle_57.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_img = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_label = Label(self, text='添加闹钟', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.rt_label.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_label.align_to(self.rt_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.layout = Widget(
            self,
            size=(240, 150),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.ROW_WRAP, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.SPACE_EVENLY, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.roller_hours = Roller(
            self.layout,
            options=("\n".join(['{:02d}'.format(hour) for hour in range(24)]), lv.roller.MODE.NORMAL),
            visible_row_count=3,
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.SELECTED | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.roller_hours.add_flag(lv.OBJ_FLAG_FLEX_IN_NEW.TRACK)
        self.roller_hours.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_hours.add_style(arial55_style, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_hours.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_hours.set_style_text_opa(lv.OPA._80, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_hours.add_event_cb(
            lambda event: print('roller_hours VALUE_CHANGED'),
            lv.EVENT.VALUE_CHANGED,
            None
        )
        self.sep = Label(self.layout, text=':')
        self.sep.add_style(arial55_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_minutes = Roller(
            self.layout,
            options=("\n".join(['{:02d}'.format(hour) for hour in range(60)]), lv.roller.MODE.NORMAL),
            visible_row_count=3,
            style_border_width=(0, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_text_color=(lv.color_white(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_color=(lv.color_black(), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_bg_opa=(lv.OPA.TRANSP, lv.PART.SELECTED | lv.STATE.DEFAULT),
            style_pad_all=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.roller_minutes.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_minutes.add_style(arial55_style, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_minutes.set_style_text_opa(lv.OPA.COVER, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller_minutes.set_style_text_opa(lv.OPA._80, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller_minutes.add_event_cb(
            lambda event: print('roller_minutes VALUE_CHANGED'),
            lv.EVENT.VALUE_CHANGED,
            None
        )

        self.btn1 = Image(self, src=self.BTN_ICON_SRC)
        self.btn1.align_to(self.layout, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        self.btn1label = Label(self.btn1, text='设置重复模式')
        self.btn1label.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn1label.set_align(lv.ALIGN.CENTER)
        self.btn2 = Image(self, src=self.BTN_ICON_SRC)
        self.btn2.align_to(self.layout, lv.ALIGN.OUT_BOTTOM_MID, 0, 55)
        self.btn2label = Label(self.btn2, text='删除闹钟')
        self.btn2label.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn2label.set_align(lv.ALIGN.CENTER)
        self.btn2label.set_style_text_color(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN | lv.STATE.DEFAULT)


class SettingItem(Widget):

    def __init__(self, parent, icon='', text=''):
        super().__init__(parent, size=(228, 50))
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.icon = Image(self, src=icon)
        self.text = Label(self, text=text)
        self.text.add_style(arial27_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text.align_to(self.icon, lv.ALIGN.OUT_RIGHT_MID, 10, 0)
        self.add_event_cb(self.event_clicked_handler, lv.EVENT.CLICKED, None)

    def event_clicked_handler(self, event):
        print('{} {} event_clicked_handler'.format(type(self).__name__, self.text.get_text()))


class SettingScreen(Widget):
    RT_ICON_SRC = 'E:/media/chevron-left-y.png'
    RECT_IMG_SRC = 'E:/media/Rectangle_54.png'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.rt_img = Image(self, src=self.RT_ICON_SRC, align=lv.ALIGN.TOP_LEFT)
        self.rt_label = Label(self, text='设置', style_text_color=(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.MAIN | lv.STATE.DEFAULT))
        self.rt_label.add_style(arial18_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.rt_label.align_to(self.rt_img, lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        self.time = Label(self, text='09:00', align=lv.ALIGN.TOP_RIGHT)

        self.layout = Widget(
            self,
            size=(240, 250),
            y=30,
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.COLUMN, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_main_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_cross_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_flex_track_place=(lv.FLEX_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT),
        )
        self.layout.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.about = SettingItem(self.layout, icon='E:/media/img_about.png', text='关于')
        self.alarm = SettingItem(self.layout, icon='E:/media/img_alarm.png', text='闹钟')
        self.message = SettingItem(self.layout, icon='E:/media/img_message_small.png', text='微信')
        self.notify = SettingItem(self.layout, icon='E:/media/img_notify.png', text='通知')
