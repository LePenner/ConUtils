import os
import asyncio

from conutils.entity.container.container import Container
from conutils.entity.elements.animated import Animated


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

    @staticmethod
    def _get_animated_obj(children):
        for child in children:
            if child:
                return child._children

    @staticmethod
    def draw(Entity):
        return print()

    def run(self):
        os.system('cls')
        self.hide_cursor()
        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            self.show_cursor()

    async def _run_async(self):

        children = self._collect_children()

        # start all loops
        for child in children:
            if hasattr(child, '_animation_loop'):
                asyncio.create_task(child._animation_loop())

        # check for updates
        while True:
            await asyncio.sleep(0.008)
            for child in children:
                if hasattr(child, '_animation_loop'):
                    if child.get_draw_flag() == True:
                        child.reset_drawflag()
                        print(child.draw_next(), end='\r')

                    pass
