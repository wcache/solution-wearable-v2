from usr.quecframe.core.pathlib import PurePath, Path


if __name__ == '__main__':
    p1 = PurePath('/../k/l/.././a/////b/cf/v//.././././././/g/')
    print('p1: "{}"'.format(p1))
    p2 = p1 / PurePath('./z/bh/v1/d3/11.txt')
    print('p2: "{}"'.format(p2))
    print('p2.parts: {}'.format(p2.parts))
    print('p2.name: "{}"'.format(p2.name))
    print('p2.suffix: "{}"'.format(p2.suffix))
    print('p2.stem: "{}"'.format(p2.stem))
    print('p2.with_name("22.txt"): "{}"'.format(p2.with_name('22.txt')))
    print('p2.with_stem("33"): "{}"'.format(p2.with_stem('33')))
    print('p2.with_suffix(".jpg"): "{}"'.format(p2.with_suffix('.jpg')))
    print('p2.parent: "{}"'.format(p2.parent))
    p = Path()
    print('iterdir: {}'.format([_ for _ in p.iterdir()]))
    print('cwd: {}'.format(Path.getcwd()))
