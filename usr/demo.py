import uos
from usr.qframe import Application
from usr.ui import gui


def mount_flash():
    ldev = uos.VfsLfs1(32, 32, 32, "ext_fs", 0, 0)
    uos.mount(ldev, '/ext')


def create_app(name='demo', version='1.0.0', config_path='/usr/default.json'):
    _app = Application(name, version=version)
    _app.config.init(config_path)

    gui.init_app(_app)

    return _app


if __name__ == '__main__':
    mount_flash()
    app = create_app()
    app.run()
