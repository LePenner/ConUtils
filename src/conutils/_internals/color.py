from xmlrpc.client import boolean


class Colors:
    """Store custom colors"""

    _colors: dict[str, tuple[int, int, int]] = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 128, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "gray": (128, 128, 128),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "brown": (165, 42, 42),
        "pink": (255, 192, 203),
        "lime": (0, 255, 0),
        "navy": (0, 0, 128),
        "gold": (255, 215, 0)
    }

    @classmethod
    def get_colors(cls):
        return cls._colors

    @classmethod
    def add_color(cls, replace: boolean = False) -> None:
        pass

    @classmethod
    def color(cls, color: str):
        if color in cls._colors.keys():
            return cls._colors[color]
        else:
            raise TypeError("Color does not exist")


print("\033[38;2;{};{};{}m".format(*Colors.color("purple")))

print("das ist ein test")
