class ColorMeta(type):

    __colors: dict[str, tuple[int, int, int]] = {}

    def __getitem__(cls, key: str) -> tuple[int, int, int]:
        return cls.__colors[key]

    def __iter__(cls):
        return iter(cls.__colors.items())

    @property
    def colors(cls):
        return cls.__colors.copy()

    @classmethod
    def add_color(cls, name: str, rgb: tuple[int, int, int], replace: bool = False):
        if name in cls.__colors and not replace:
            raise Exception("IMPLEMENT color not in colors")
        setattr(cls, name, rgb)
        cls.__colors[name] = rgb


class Color(metaclass=ColorMeta):
    pass


default_colors: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255)
}

for name, value in default_colors.items():
    Color.add_color(name, value)
