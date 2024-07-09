import utime
import _thread
from machine import Pin
from misc import Power

gpio1 = Pin(Pin.GPIO20, Pin.OUT, Pin.PULL_DISABLE, 1)
gpio2 = Pin(Pin.GPIO37, Pin.OUT, Pin.PULL_DISABLE, 1)
gpio3 = Pin(Pin.GPIO44, Pin.OUT, Pin.PULL_DISABLE, 1)
Power.camVDD2V8Enable(1)

test = (
    2, 0, 120,
    0, 0, 0x11,
    0, 1, 0x36,
    1, 1, 0x00,
    # 0, 1, 0x36,
    # 1, 1, 0x00,
    0, 1, 0x3A,
    1, 1, 0x05,
    0, 0, 0x21,
    0, 5, 0xB2,
    1, 1, 0x05,
    1, 1, 0x05,
    1, 1, 0x00,
    1, 1, 0x33,
    1, 1, 0x33,
    0, 1, 0xB7,
    1, 1, 0x23,
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
    1, 1, 0x0F,
    0, 2, 0xD0,
    1, 1, 0xA4,
    1, 1, 0xA1,
    0, 1, 0xD6,
    1, 1, 0xA1,
    0, 14, 0xE0,
    1, 1, 0x70,
    1, 1, 0x06,
    1, 1, 0x0C,
    1, 1, 0x08,
    1, 1, 0x09,
    1, 1, 0x27,
    1, 1, 0x2E,
    1, 1, 0x34,
    1, 1, 0x46,
    1, 1, 0x37,
    1, 1, 0x13,
    1, 1, 0x13,
    1, 1, 0x25,
    1, 1, 0x2A,
    0, 14, 0xE1,
    1, 1, 0x70,
    1, 1, 0x04,
    1, 1, 0x08,
    1, 1, 0x09,
    1, 1, 0x07,
    1, 1, 0x03,
    1, 1, 0x2C,
    1, 1, 0x42,
    1, 1, 0x42,
    1, 1, 0x38,
    1, 1, 0x14,
    1, 1, 0x14,
    1, 1, 0x27,
    1, 1, 0x2C,
    0, 0, 0x29,
    0, 4, 0x2a,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0xef,
    0, 4, 0x2b,
    1, 1, 0x00,
    1, 1, 0x00,
    1, 1, 0x01,
    1, 1, 0x3f,
    0, 0, 0x2c,

)

XSTART_H = 0xf0
XSTART_L = 0xf1
YSTART_H = 0xf2
YSTART_L = 0xf3
XEND_H = 0xE0
XEND_L = 0xE1
YEND_H = 0xE2
YEND_L = 0xE3

XSTART = 0xD0
XEND = 0xD1
YSTART = 0xD2
YEND = 0xD3

from machine import LCD
import utime

lcd = LCD()

test1 = bytearray(test)

test2 = (
    0, 4, 0x2a,
    1, 1, XSTART_H,
    1, 1, XSTART_L,
    1, 1, XEND_H,
    1, 1, XEND_L,
    0, 4, 0x2b,
    1, 1, YSTART_H,
    1, 1, YSTART_L,
    1, 1, YEND_H,
    1, 1, YEND_L,
    0, 0, 0x2c,
)
test_invalid = bytearray(test2)

test3 = (
    0, 0, 0x28,
    2, 0, 120,
    0, 0, 0x10,
)
test_displayoff = bytearray(test3)

test4 = (
    0, 0, 0x11,
    2, 0, 20,
    0, 0, 0x29,
)
test_displayon = bytearray(test4)


lcd.lcd_init(test1, 240, 320, 26000, 1, 4, 0, test_invalid, test_displayon, test_displayoff, None)
# lcd.lcd_init(test1, 240, 320, 5, 1, 4, 0, test_invalid, test_displayon, test_displayoff, None, 1, 0, 0, 2, 28, 29)
# lcd.lcd_init(test1, 240,320,4,1,4,0,test_invalid,test_displayon,test_displayoff,None,1, 0, 0, 2, 4, 31)
# res = lcd.readID(0x3a)
# print(res)
# utime.sleep(2)
lcd.lcd_clear(0xF800)
# lcd.lcd_brightness(5)
lcd.lcd_display_on()


# -----------------------------------------

import lvgl as lv
lv.init()
lv.extra_init()
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytes(240*320*2)
disp_buf1.init(buf1_1, None, len(buf1_1))
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = lcd.lcd_write
disp_drv.hor_res = 240              #此处基于实际的屏幕来设置水平分辨率
disp_drv.ver_res = 320              #此处基于实际的屏幕来设置垂直分辨率
disp_drv.register()
lv.tick_inc(5)
lv.task_handler()

light_color_style_screen = lv.style_t()
light_color_style_screen.init()
light_color_style_screen.set_bg_color(lv.color_make(0xff, 0xff, 0xff))
light_color_style_screen.set_bg_opa(255)


style_font_black_montserrat_16 = lv.style_t()
style_font_black_montserrat_16.init()
style_font_black_montserrat_16.set_radius(0)
style_font_black_montserrat_16.set_bg_color(lv.color_make(0x21, 0x95, 0xf6))
style_font_black_montserrat_16.set_bg_grad_color(lv.color_make(0x21, 0x95, 0xf6))
style_font_black_montserrat_16.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_font_black_montserrat_16.set_bg_opa(0)
style_font_black_montserrat_16.set_text_color(lv.color_make(0x00, 0x00, 0x00))

# 参数1：字体文件路径
# 参数2：字体大小
# 参数3：0：标准，1：斜体，2：粗体
style_font_black_montserrat_16.set_freetype_text_font("U:/mynewfont3.ttf", 24, 1)
# style_font_black_montserrat_16.set_text_font_v2("lv_font_18.bin", 24, 0)#EC810 1 EC800 2
style_font_black_montserrat_16.set_text_letter_space(0)
style_font_black_montserrat_16.set_pad_left(0)
style_font_black_montserrat_16.set_pad_right(0)
style_font_black_montserrat_16.set_pad_top(0)
style_font_black_montserrat_16.set_pad_bottom(0)

style_font_black_montserrat_17 = lv.style_t()
style_font_black_montserrat_17.init()
style_font_black_montserrat_17.set_radius(0)
style_font_black_montserrat_17.set_bg_color(lv.color_make(0x21, 0x95, 0xf6))
style_font_black_montserrat_17.set_bg_grad_color(lv.color_make(0x21, 0x95, 0xf6))
style_font_black_montserrat_17.set_bg_grad_dir(lv.GRAD_DIR.VER)
style_font_black_montserrat_17.set_bg_opa(0)
style_font_black_montserrat_17.set_text_color(lv.color_make(0x00, 0x00, 0x00))
print(111111)
style_font_black_montserrat_17.set_freetype_text_font("U:/mynewfont3.ttf", 16, 1)
print(222222222)
style_font_black_montserrat_17.set_text_letter_space(0)
style_font_black_montserrat_17.set_pad_left(0)
style_font_black_montserrat_17.set_pad_right(0)
style_font_black_montserrat_17.set_pad_top(0)
style_font_black_montserrat_17.set_pad_bottom(0)


welcome_screen = lv.obj()
welcome_screen.add_style(light_color_style_screen, lv.PART.MAIN | lv.STATE.DEFAULT)


# 在第一个界面中创建一个label
welcome_label = lv.label(welcome_screen)
# 给这个label设置文本内容
welcome_label.set_text("中国梦")
# 设置字体样式
welcome_label.add_style(style_font_black_montserrat_16, lv.PART.MAIN | lv.STATE.DEFAULT)
# 将文本内容置于文本框的中间
welcome_label.center()

# 在第一个界面中创建一个label
welcome_label2 = lv.label(welcome_screen)
# 给这个label设置文本内容
welcome_label2.set_text("中国梦")
# 设置字体样式
welcome_label2.add_style(style_font_black_montserrat_17, lv.PART.MAIN | lv.STATE.DEFAULT)


lv.scr_load(welcome_screen)

