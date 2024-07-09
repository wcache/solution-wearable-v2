import lvgl as lv
from .core import Type


class Widget(Type(lv.obj)):
    pass


class Arc(Type(lv.arc)):
    pass


class Bar(Type(lv.bar)):
    pass


class Button(Type(lv.btn)):

    def __init__(self, *args, **kwargs):
        text = kwargs.pop('text', 'Button')
        super().__init__(*args, **kwargs)
        self.label = Label(self, text=text, style_align=(lv.ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT))


class ButtonMatrix(Type(lv.btnmatrix)):
    pass


class Canvas(Type(lv.canvas)):
    pass


class Checkbox(Type(lv.checkbox)):
    pass


class DropDownList(Type(lv.dropdown)):
    pass


class Image(Type(lv.img)):
    pass


class Label(Type(lv.label)):
    pass


class Line(Type(lv.line)):
    pass


class Roller(Type(lv.roller)):
    pass


class Slider(Type(lv.slider)):
    pass


class Switch(Type(lv.switch)):
    pass


class Table(Type(lv.table)):
    pass


class TextArea(Type(lv.textarea)):
    pass


class AnimationImage(Type(lv.animimg)):
    pass


class Calendar(Type(lv.calendar)):
    pass


class Chart(Type(lv.chart)):
    pass


class ColorWheel(Type(lv.colorwheel)):
    pass


class ImageButton(Type(lv.imgbtn)):
    pass


class Keyboard(Type(lv.keyboard)):
    pass


class LED(Type(lv.led)):
    pass


class List(Type(lv.list)):
    pass


# class Menu(Type(lv.menu)):
#     pass


class Meter(Type(lv.meter)):
    pass


class MessageBox(Type(lv.msgbox)):
    pass


# class Span(Type(lv.span)):
#     pass


class Spinbox(Type(lv.spinbox)):
    pass


class Spinner(Type(lv.spinner)):
    pass


class Tabview(Type(lv.tabview)):
    pass


class TileView(Type(lv.tileview)):
    pass


class Window(Type(lv.win)):
    pass
