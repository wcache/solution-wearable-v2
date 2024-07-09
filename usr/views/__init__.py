from usr.qframe.ui import Gui
from usr.qframe.logging import getLogger

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
