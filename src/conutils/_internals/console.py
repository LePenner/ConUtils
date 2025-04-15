from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity

import os
import asyncio

from .entity.container import Container
from .entity.elements import Animated
from .color import Colors


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal."""

    def __init__(self, overlap: bool = False):
        self._children = []

        super().__init__(parent=None,
                         x=0,
                         y=0,
                         width=os.get_terminal_size()[0],
                         height=os.get_terminal_size()[1],
                         overlap=overlap)

    @staticmethod
    def _draw(entity: Entity):
        # terminal starts at 1,1
        print(f"\033[{entity.y_abs+1};{entity.x_abs+1}H", end="")
        print(entity, end="", flush=True)

    @staticmethod
    def hide_cursor():
        print('\033[?25l', end="", flush=True)

    @staticmethod
    def show_cursor():
        print('\033[?25h')

    @staticmethod
    def clear_console():
        print("\033[2J", end="", flush=True)

    @staticmethod
    def set_color(color: str):
        print("\033[38;2;{};{};{}m".format(*Colors.color(color)))

    def run(self):
        self.clear_console()
        self.hide_cursor()
        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            self.show_cursor()
            self.clear_console()

    async def _run_async(self):

        children = self._collect_children()

        # start all loops
        for child in children:
            if isinstance(child, Animated):
                # _animation_loop() is protected
                asyncio.create_task(child._animation_loop())  # type: ignore

        # check for updates
        while True:
            await asyncio.sleep(0.0001)
            for child in children:
                if isinstance(child, Animated):
                    if child.draw_flag == True:
                        child.reset_drawflag()
                        child.draw_next()

                self._draw(child)
