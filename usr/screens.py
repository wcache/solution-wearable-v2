"""表盘"""
import lvgl as lv
from usr.qframe.ui import Gui
from usr.qframe.logging import getLogger
from usr.qframe.collections import Singleton
from usr.qframe.ui.widgets import Widget, Label
from usr.qframe.ui.core import Style


logger = getLogger(__name__)


class GuiService(Gui):

    def __init__(self, app=None):
        super().__init__()
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.register('gui', self)

    def load(self):
        logger.debug('load {}'.format(type(self).__name__))
        self.init()


gui = GuiService()


class Font(object):
    flash_port = 0
    db = {}

    @classmethod
    def get_font_by_name(cls, name):
        # name: <字体名称> + <子模高度>
        height = int(name.split('_')[-1])
        lv_font = lv.style_t()
        lv_font.init()
        lv_font.set_text_font_v2("{}.bin".format(name), height, cls.flash_port)
        return lv_font

    @classmethod
    def get(cls, font_name):
        if font_name not in cls.db:
            cls.db[font_name] = cls.get_font_by_name(font_name)
        return cls.db[font_name]


normal_style = Style(
    border_width=0,
    pad_all=0,
    outline_width=0,
    text_color=lv.color_white(),
    radius=0,
    bg_color=lv.color_black()
)


@Singleton
class DialPlateScreen(Widget):

    def __init__(self):
        super().__init__(None)
        self.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.text = Label(self, text=type(self).__name__)

