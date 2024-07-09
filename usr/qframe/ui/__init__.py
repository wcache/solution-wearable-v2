import lvgl as lv
# from tp import cst816 as Cst816
from machine import Pin, LCD


# -------------LCD屏幕参数配置--------------

LCD_INIT_DATA = bytes(
    (
        0, 0, 0x11,
        2, 0, 120,
        0, 1, 0x36,
        1, 1, 0x00,
        0, 1, 0x3A,
        1, 1, 0x05,
        0, 5, 0xB2,
        1, 1, 0x05,
        1, 1, 0x05,
        1, 1, 0x00,
        1, 1, 0x33,
        1, 1, 0x33,
        0, 1, 0xB7,
        1, 1, 0x75,
        0, 1, 0xBB,
        1, 1, 0x22,
        0, 1, 0xC0,
        1, 1, 0x2C,
        0, 1, 0xC2,
        1, 1, 0x01,
        0, 1, 0xC3,
        1, 1, 0x13,
        0, 1, 0xC4,
        1, 1, 0x20,
        0, 1, 0xC6,
        1, 1, 0x11,
        0, 2, 0xD0,
        1, 1, 0xA4,
        1, 1, 0xA1,
        0, 1, 0xD6,
        1, 1, 0xA1,
        0, 14, 0xE0,
        1, 1, 0xD0,
        1, 1, 0x05,
        1, 1, 0x0A,
        1, 1, 0x09,
        1, 1, 0x08,
        1, 1, 0x05,
        1, 1, 0x2E,
        1, 1, 0x44,
        1, 1, 0x45,
        1, 1, 0x0F,
        1, 1, 0x17,
        1, 1, 0x16,
        1, 1, 0x2B,
        1, 1, 0x33,
        0, 14, 0xE1,
        1, 1, 0xD0,
        1, 1, 0x05,
        1, 1, 0x0A,
        1, 1, 0x09,
        1, 1, 0x08,
        1, 1, 0x05,
        1, 1, 0x2E,
        1, 1, 0x43,
        1, 1, 0x45,
        1, 1, 0x0F,
        1, 1, 0x16,
        1, 1, 0x16,
        1, 1, 0x2B,
        1, 1, 0x33,
        0, 0, 0x29,
        0, 0, 0x21
    )
)

LCD_INVALID = bytes(
    (
        0, 4, 0x2a,
        1, 1, 0xf0,
        1, 1, 0xf1,
        1, 1, 0xE0,
        1, 1, 0xE1,
        0, 4, 0x2b,
        1, 1, 0xf2,
        1, 1, 0xf3,
        1, 1, 0xE2,
        1, 1, 0xE3,
        0, 0, 0x2c,
    )
)

LCD_DISPLAY_OFF = bytes(
    (
        0, 0, 0x11,
        2, 0, 20,
        0, 0, 0x29,
    )
)

LCD_DISPLAY_ON = bytes(
    (
        0, 0, 0x28,
        2, 0, 120,
        0, 0, 0x10,
    )
)

LCD_WIDTH = 240
LCD_HEIGHT = 320
LCD_CLK = 26000
DATA_LINE = 1
LINE_NUM = 4
LCD_TYPE = 0
LCD_SET_BRIGHTNESS = None


# -------------GUI初始化--------------


class Gui(object):
    """lcd、lvgl、tp初始化"""

    def __init__(self):
        self.lcd = None
        self.tp = None
        self.lv = None
        self.indev_drv = None
        self.disp_drv = None

    def init_app(self, app):
        app.register('gui', self)

    def init(self):
        self.lcd = self.init_lcd()
        # self.tp = self.init_tp()
        self.lv, self.disp_drv, self.indev_drv = self.init_lvgl(self.lcd, self.tp)

    @staticmethod
    def init_lcd():
        lcd = LCD()
        lcd.lcd_init(
            LCD_INIT_DATA,
            LCD_WIDTH,
            LCD_HEIGHT,
            LCD_CLK,
            DATA_LINE,
            LINE_NUM,
            LCD_TYPE,
            LCD_INVALID,
            LCD_DISPLAY_ON,
            LCD_DISPLAY_OFF,
            LCD_SET_BRIGHTNESS
        )
        return lcd

    @staticmethod
    def init_tp():
        Pin(44, Pin.OUT, Pin.PULL_DISABLE, 1)
        Pin(31, Pin.OUT, Pin.PULL_DISABLE, 1)
        tp_cst816 = Cst816(i2c_no=0, irq=44, reset=31, addr=0x15)
        tp_cst816.init()
        # tp_cst816.set_callback(self.ui_callback)
        tp_cst816.activate()
        return tp_cst816

    @staticmethod
    def init_lvgl(lcd, tp):
        lv.init()

        # init display driver
        disp_buf = lv.disp_draw_buf_t()
        buf_length = LCD_WIDTH * LCD_HEIGHT * 2
        disp_buf.init(bytearray(buf_length), None, buf_length)
        # disp_buf1.init(bytearray(buf_length), bytearray(buf_length), buf_length)  # 双buffer缓冲，占用过多RAM
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf
        disp_drv.flush_cb = lcd.lcd_write
        disp_drv.hor_res = LCD_WIDTH
        disp_drv.ver_res = LCD_HEIGHT
        # disp_drv.sw_rotate = 1  # 此处设置是否需要旋转
        # disp_drv.rotated = lv.DISP_ROT._270  # 旋转角度
        disp_drv.register()

        # init input driver
        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.type = lv.INDEV_TYPE.POINTER
        # indev_drv.read_cb = tp.read
        indev_drv.long_press_time = 400  # 400，表示长按的时间阈值，即按住一个点的时间超过该值时，触发长按事件。
        indev_drv.scroll_limit = 10  # 10，表示在拖动对象之前，需要滑动的像素数。
        indev_drv.scroll_throw = 10  # 10，表示滚动减速的百分比，值越大则减速越快。
        indev_drv.gesture_limit = 10  # 50，表示手势滑动的阈值，即只有滑动偏移累计（绝对值）超过这个值才会触发手势动作。
        indev_drv.gesture_min_velocity = 3  # 3，表示判断手势触发的最小差值。
        indev_drv.register()
        Pin(44, Pin.OUT, Pin.PULL_DISABLE, 0)

        # image cache
        lv.img.cache_invalidate_src(None)
        lv.img.cache_set_size(50)

        # start lvgl thread
        lv.tick_inc(5)
        lv.task_handler()

        return lv, disp_drv, indev_drv

    @staticmethod
    def ui_callback(para):
        if para == 0:
            print("tp: <-")
        elif para == 1:
            print("tp: ->")
        elif para == 2:
            print("tp: ^")
        elif para == 3:
            print("tp: V")
        elif para == 4:
            print("tp: return")
        elif para == 5:
            print("tp: CLICK")
        elif para == 6:
            print("tp: error")
