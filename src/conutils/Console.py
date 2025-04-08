import os

from conutils.entity.container.container import Container


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal."""

    def __init__(self):
        self._children = []
        super().__init__(parent=None,
                         x=0,
                         y=0,
                         width=os.get_terminal_size()[0],
                         height=os.get_terminal_size()[1])

    @staticmethod
    def hide_cursor():
        print('\033[?25l', end="")

    @staticmethod
    def show_cursor():
        print('\033[?25h', end="")
