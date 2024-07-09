"""lvgl implement for QuecPython based on lvgl 8.3 <https://docs.lvgl.io/8.3/>"""
import lvgl as lv


class AnimTimeline(object):

    def __init__(self):
        self.__obj = lv.anim_timeline_create()

    @property
    def obj(self):
        return self.__obj

    def add(self, start_time, anim):
        return lv.anim_timeline_add(self.obj, start_time, anim)

    def start(self):
        return lv.anim_timeline_start(self.obj)

    def set_reverse(self, reverse):
        return lv.anim_timeline_set_reverse(self.obj, reverse)

    # def stop(self):
    #     lv.anim_timeline_stop(self.obj)

    def set_progress(self, progress):
        return lv.anim_timeline_set_progress(self.obj, progress)

    def get_playtime(self):
        return lv.anim_timeline_get_playtime(self.obj)

    def get_reverse(self):
        return lv.anim_timeline_get_reverse(self.obj)

    def delete(self):
        return lv.anim_timeline_del(self.obj)


class Anim(lv.anim_t):

    def __init__(self, var, values, time, **options):
        super().__init__()
        self.init()
        self.set_var(var)  # WARNING: var should be set at first time, if not, sometimes will crush, I don't know why
        self.set_values(*values)
        self.set_time(time)
        for option, value in options.items():
            getattr(self, 'set_' + option)(*(value if isinstance(value, (list, tuple)) else (value, )))


class StyleTransitionDsc(lv.style_transition_dsc_t):

    def __init__(self, trans_props, duration_ms, delay_ms=0, anim_path=lv.anim_t.path_ease_in_out, user_data=None):
        super().__init__()
        self.init(trans_props, anim_path, duration_ms, delay_ms, user_data)


class Style(lv.style_t):

    def __init__(self, **options):
        super().__init__()
        self.init()
        for option, value in options.items():
            getattr(self, 'set_' + option)(*(value if isinstance(value, (tuple, list)) else (value, )))


def show(self):
    self.clear_flag(lv.obj.FLAG.HIDDEN)


def hidden(self):
    self.add_flag(lv.obj.FLAG.HIDDEN)


def get_pos(self):
    return self.get_x(), self.get_y()


def get_size(self):
    return self.get_width(), self.get_height()


def load(self):
    lv.scr_load(self)


def load_anim(self, time, delay=0, transition_type=lv.SCR_LOAD_ANIM.OVER_LEFT, auto_del=False):
    lv.scr_load_anim(self, transition_type, time, delay, auto_del)


def __str__(self):
    return '<{}.{} object at {}>'.format(__name__, type(self).__name__, id(self))


def Type(metaclass):

    class cls(metaclass):

        def __init__(self, parent, *args, **options):
            super().__init__(parent, *args)
            for option, value in options.items():
                getattr(self, 'set_' + option)(*(value if isinstance(value, (list, tuple)) else (value, )))
            self.set_user_data(self)  # lv.scr_act() return `self`

    setattr(cls, '__str__', __str__)
    setattr(cls, 'show', show)
    setattr(cls, 'hidden', hidden)
    setattr(cls, 'load', load)
    setattr(cls, 'get_pos', get_pos)
    setattr(cls, 'load_anim', load_anim)
    setattr(cls, 'get_size', get_size)

    return cls
