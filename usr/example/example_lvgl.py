import lvgl as lv
from usr.ui import *
from usr.ui.widgets import *
from usr.ui.core import *


# 通用风格
normal_style = Style(
    width=100,
    height=100,
    align=lv.ALIGN.CENTER,
    radius=0,
    bg_color=lv.palette_main(lv.PALETTE.BLUE),
    text_color=lv.palette_main(lv.PALETTE.RED),
    pad_all=10,
    border_width=10,
    border_color=lv.palette_main(lv.PALETTE.ORANGE),
    outline_width=10,
    outline_color=lv.palette_main(lv.PALETTE.PINK),
    shadow_color=lv.palette_main(lv.PALETTE.GREEN),
    shadow_width=10,
    shadow_ofs_x=0,
    shadow_ofs_y=0,
    shadow_spread=0,
    shadow_opa=lv.OPA.COVER,
)


# 带有过渡动画的风格
transition_style = Style(
    width=150,
    height=60,
    bg_color=lv.palette_main(lv.PALETTE.RED),
    translate_x=50,
    translate_y=50,
    transition=StyleTransitionDsc(
        [
            lv.STYLE.WIDTH,
            lv.STYLE.HEIGHT,
            lv.STYLE.BG_COLOR,
            lv.STYLE.TRANSLATE_X,
            lv.STYLE.TRANSLATE_Y,
        ],
        duration_ms=500,
        delay_ms=0,
        # anim_path=lv.anim_t.path_step,  # 无特效
        # anim_path=lv.anim_t.path_overshoot,  # 回弹
        # anim_path=lv.anim_t.path_bounce,  # 回弹(多弹几次)
        # anim_path=lv.anim_t.path_linear,  # 等速
        anim_path=lv.anim_t.path_ease_in_out,  # 先慢，后快，再慢
        # anim_path=lv.anim_t.path_ease_in,  # 先慢，后快
        # anim_path=lv.anim_t.path_ease_out,  # 先快，后慢
        user_data=None
    )
)


# 背景图片
wallpaper_style = Style(
    bg_img_src='E:/img/img_lock_bg.png',
    bg_img_opa=lv.OPA.COVER,
    bg_img_recolor=lv.palette_main(lv.PALETTE.LIGHT_GREEN),
    bg_img_recolor_opa=lv.OPA.TRANSP,
    bg_img_tiled=True
)


class WallPaperExample(Widget):

    def __init__(self):
        super().__init__(None, size=(240, 320))
        self.add_style(wallpaper_style, lv.PART.MAIN | lv.STATE.DEFAULT)


class ScrollExample(Widget):

    def __init__(self):
        super().__init__(
            None,
            size=(240, 320),
            layout=lv.LAYOUT_FLEX.value,
            style_flex_flow=(lv.FLEX_FLOW.COLUMN, lv.PART.MAIN | lv.STATE.DEFAULT),
            scroll_snap_x=lv.SCROLL_SNAP.START,  # 滚动时，x轴方向对齐，START（左），END（右），CENTER(中)
            scroll_snap_y=lv.SCROLL_SNAP.START  # 滚动时，y轴方向对齐，START（上），END（下），CENTER(中)
        )
        # self.add_flag(lv.obj.FLAG.SCROLL_ELASTIC)  # 弹簧拉伸效果（开）
        self.clear_flag(lv.obj.FLAG.SCROLL_ELASTIC)  # 弹簧拉伸效果（关）
        # self.add_flag(lv.obj.FLAG.SCROLL_MOMENTUM)  # 惯性效果（开）
        self.clear_flag(lv.obj.FLAG.SCROLL_MOMENTUM)  # 惯性效果（关）
        # self.add_flag(lv.obj.FLAG.SCROLL_ONE)  # 一次只滚动一个child（需要设置snap对齐方式）（开）
        self.clear_flag(lv.obj.FLAG.SCROLL_ONE)  # 一次只滚动一个child（需要设置snap对齐方式）（关）
        # self.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)  # 聚焦时自动滚动（child不在可视范围时自动滚动到可是范围）（开）
        self.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)  # 聚焦时自动滚动（child不在可视范围时自动滚动到可是范围）（关）

        # 手动滚动
        # self.scroll_by(x, y, LV_ANIM_ON/OFF) scroll by x and y values
        # self.scroll_to(x, y, LV_ANIM_ON/OFF) scroll to bring the given coordinate to the top left corner
        # self.scroll_to_x(x, LV_ANIM_ON/OFF) scroll to bring the given coordinate to the left side
        # self.scroll_to_y(y, LV_ANIM_ON/OFF) scroll to bring the given coordinate to the top side
        # 获取坐标
        # self.get_scroll_x() Get the x coordinate of object
        # self.get_scroll_y() Get the y coordinate of object
        # self.get_scroll_top() Get the scroll coordinate from the top
        # self.get_scroll_bottom() Get the scroll coordinate from the bottom
        # self.get_scroll_left() Get the scroll coordinate from the left
        # self.get_scroll_right() Get the scroll coordinate from the right

        for i in range(5):
            w = Widget(self, style_bg_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT))
            if i % 2:
                w.set_size(200, 100)
            else:
                w.set_size(200, 60)
            w.add_event_cb(lambda _: print('clicked!!! {}'.format(_.get_target())), lv.EVENT.CLICKED, None)


class BoxModelExample(Widget):

    def __init__(self):
        super().__init__(None, size=(240, 320))

        self.w = Widget(self)
        self.w.add_style(normal_style, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.content_widget = Widget(
            self.w,
            size=(60, 60),
            style_border_width=(0, 0),
            style_pad_all=(0, 0),
            style_align=(lv.ALIGN.TOP_LEFT, lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        )


class SlideMenuExample(Widget):

    def __init__(self):
        super().__init__(None)
        self.left_menu = Widget(
            self,
            size=(120, 320),
            x=-120,  # make it invisible
            style_bg_color=(lv.palette_main(lv.PALETTE.RED), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.left_menu_anim = Anim(
            var=self.left_menu,
            values=(0, -120),
            time=200,
            path_cb=lv.anim_t.path_ease_out,
            custom_exec_cb=lambda anim, value: self.left_menu.set_x(value)
        )

        self.top_menu = Widget(
            self,
            size=(240, 160),
            y=-160,  # make it invisible
            style_bg_color=(lv.palette_main(lv.PALETTE.GREEN), lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.top_menu_anim = Anim(
            var=self.top_menu,
            values=(0, -160),
            time=200,
            path_cb=lv.anim_t.path_ease_out,
            custom_exec_cb=lambda anim, value: self.top_menu.set_y(value)
        )

        self.add_event_cb(self.__change_slide_menu, lv.EVENT.GESTURE, None)

    def __change_slide_menu(self, event):
        indev = event.get_indev()
        direction = indev.get_gesture_dir()

        if direction == lv.DIR.TOP:
            if self.top_menu.get_y() < 0 or self.left_menu.get_x() >= 0:
                return
            self.top_menu_anim.set_values(0, -160)
            self.top_menu_anim.start()
        elif direction == lv.DIR.BOTTOM:
            if self.top_menu.get_y() >= 0 or self.left_menu.get_x() >= 0:
                return
            self.top_menu_anim.set_values(-160, 0)
            self.top_menu_anim.start()
        elif direction == lv.DIR.LEFT:
            if self.left_menu.get_x() < 0 or self.top_menu.get_y() >= 0:
                return
            self.left_menu_anim.set_values(0, -120)
            self.left_menu_anim.start()
        elif direction == lv.DIR.RIGHT:
            if self.left_menu.get_x() >= 0 or self.top_menu.get_y() >= 0:
                return
            self.left_menu_anim.set_values(-120, 0)
            self.left_menu_anim.start()
        else:
            pass


class AnimExample(Widget):

    def __init__(self):
        super().__init__(None)
        self.c = Widget(
            self,
            size=(50, 50),
            pos=(50, 50),
            style_bg_color=(lv.palette_main(lv.PALETTE.PURPLE), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT)
        )

        Anim(
            var=self.c,  # 动画关联对象
            values=(50, 100),  # 动态改变的值
            time=500,  # 动画总时长ms
            delay=1000,  # 延迟触发ms
            playback_time=500,  # 动画回放时间ms
            playback_delay=1000,  # 延迟回放ms
            repeat_count=lv.ANIM_REPEAT.INFINITE,  # 重复次数，默认重复1次
            repeat_delay=0,  # 重复动画延迟ms
            early_apply=True,  # 是否将起始值应用到动画开始前，使动画执行时不会太突兀
            # path_cb=lv.anim_t.path_step,  # 无特效
            # path_cb=lv.anim_t.path_overshoot,  # 回弹
            # path_cb=lv.anim_t.path_bounce,  # 回弹(多弹几次)
            # path_cb=lv.anim_t.path_linear,  # 等速
            # path_cb=lv.anim_t.path_ease_in_out,  # 先慢，后快，再慢
            # path_cb=lv.anim_t.path_ease_in,  # 先慢，后快
            path_cb=lv.anim_t.path_ease_out,  # 先快，后慢
            custom_exec_cb=self.__anim_custom_exec_cb,  # 动画执行函数
            ready_cb=lambda *args, **kwargs: print('indicate when the animation is ready: {}; {}'.format(args, kwargs)),
            start_cb=lambda *args, **kwargs: print('indicate when the animation is started (after delay): {}; {}'.format(args, kwargs))
        ).start()

    def __anim_custom_exec_cb(self, anim, value):
        self.c.set_size(value, value)
        self.c.set_pos(value, value)


class AnimExample2(Widget):

    def __init__(self):
        super().__init__(None)
        self.arc = Arc(self, value=0, range=(0, 100), rotation=270, bg_angles=(0, 360))
        self.arc.center()
        self.arc.remove_style(None, lv.PART.KNOB)
        self.arc.clear_flag(lv.obj.FLAG.CLICKABLE)

        self.label = Label(self.arc)
        self.label.center()
        self.label.set_text(str(self.arc.get_value()))

        self.anim = Anim(
            var=self.arc,
            values=(0, 100),
            time=10000,
            custom_exec_cb=self.anim_custom_exec_cb
        )

        self.add_event_cb(self.event_pressed_cb, lv.EVENT.PRESSED, None)
        self.add_event_cb(self.event_released_cb, lv.EVENT.RELEASED, None)

    def anim_custom_exec_cb(self, anim, value):
        self.arc.set_value(value)
        self.label.set_text(str(value // 10))
        if value == 100:
            self.clear_flag(lv.obj.FLAG.CLICKABLE)
            print('done!!!!')

    def event_pressed_cb(self, event):
        lv.anim_del_all()
        value = self.arc.get_value()
        self.anim.set_values(value, 100)
        self.anim.set_time((100 - value) // 10 * 1000)
        self.anim.start()

    def event_released_cb(self, event):
        lv.anim_del_all()
        value = self.arc.get_value()
        self.anim.set_values(value, 0)
        self.anim.set_time(value // 10 * 1000)
        self.anim.start()


class AnimTimelineExample(Widget):

    def __init__(self):
        super().__init__(None)

        self.w1 = Widget(
            self,
            size=(50, 50),
            pos=(20, 0),
            style_bg_color=(lv.palette_main(lv.PALETTE.PURPLE), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.anim1 = Anim(
            var=self.w1,
            values=(0, 150),
            time=1000,
            custom_exec_cb=lambda anim, value: self.w1.set_y(value)
        )

        self.w2 = Widget(
            self,
            size=(50, 50),
            pos=(80, 0),
            style_bg_color=(lv.palette_main(lv.PALETTE.ORANGE), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.anim2 = Anim(
            var=self.w2,
            values=(0, 150),
            time=1000,
            custom_exec_cb=lambda anim, value: self.w2.set_y(value)
        )

        self.w3 = Widget(
            self,
            size=(50, 50),
            pos=(140, 0),
            style_bg_color=(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN | lv.STATE.DEFAULT),
            style_radius=(90, lv.PART.MAIN | lv.STATE.DEFAULT)
        )
        self.anim3 = Anim(
            var=self.w3,
            values=(0, 150),
            time=1000,
            custom_exec_cb=lambda anim, value: self.w3.set_y(value)
        )

        self.at = AnimTimeline()
        self.at.add(0, self.anim1)
        self.at.add(1000, self.anim2)
        self.at.add(2000, self.anim3)

        self.slider = Slider(self, range=(0, 0xffff), pos=(20, 210), size=(150, 20))
        self.slider.add_event_cb(self.slider_prg_event_handler, lv.EVENT.VALUE_CHANGED, None)

        self.button = Button(self, pos=(20, 250), size=(150, 50))
        self.button.add_event_cb(self.button_clicked_event_handler, lv.EVENT.CLICKED, None)

    def button_clicked_event_handler(self, event):
        self.at.start()

    def slider_prg_event_handler(self, event):
        self.at.set_progress(self.slider.get_value())


if __name__ == '__main__':

    gui = Gui()
    gui.init()
