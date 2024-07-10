"""表盘"""
import lvgl as lv
from usr.qframe.collections import Singleton, OrderedDict
from usr.qframe.logging import getLogger
from .widgets import Widget, Label, TileView, Image
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
        self.app_list = AppList1Screen(self.tile10)


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
        self.hour_low = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=0, y=100)
        self.minute_high = Image(self.layout1, src=self.H_IMG_FORMAT.format(0), x=58, y=0)
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
class AppList1Screen(Widget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text = Label(self, text=type(self).__name__)


@Singleton
class AppList2Screen(Widget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size(240, 280)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text = Label(self, text=type(self).__name__)
