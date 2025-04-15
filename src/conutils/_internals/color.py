from xmlrpc.client import boolean


class Colors:
    """Store custom colors"""

    _colors: dict[str, tuple[int, int, int]] = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "dark_red": (139, 0, 0),
        "dark_green": (0, 100, 0),
        "dark_blue": (0, 0, 139),
        "yellow": (255, 255, 153),
        "blue": (173, 216, 230),
        "purple": (216, 191, 216),
        "gray": (128, 128, 128),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "brown": (165, 42, 42),
        "pink": (255, 192, 203),
        "green": (0, 255, 0),
        "navy_blue": (0, 0, 128),
        "gold": (255, 215, 0),

        "light_gray": (211, 211, 211),
        "olive": (128, 128, 0),
        "blue_green": (0, 128, 128),
        "red_brown": (128, 0, 0),
        "orange": (255, 160, 122),
        "pale_green": (152, 251, 152),
        "peach": (255, 218, 185),
        "deep_purple": (75, 0, 130),
        "beige": (245, 245, 220),
        "light_pink": (255, 182, 193),
        "brick_red": (203, 65, 84),
        "sky_blue": (135, 206, 250),
        "soft_purple": (218, 112, 214),
        "mint": (189, 252, 201),
        "steel_gray": (112, 128, 144),
        "dark_orange": (255, 140, 0)
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
