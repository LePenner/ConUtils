from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity

import __main__
import os
import asyncio
from .entity.container import Container
from .entity.elements import Animated


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal.

    define an `update` function to configure runtime behavior. 
    """

    def __init__(self, overlap: bool = False):
        self._stop_flag = False

        super().__init__(parent=None,
                         x=0,
                         y=0,
                         width=os.get_terminal_size()[0],
                         height=os.get_terminal_size()[1],
                         overlap=overlap)

    _draw_buffer: str = ""
    # collects areas (range, range) where to clear artifacts after moving an Entity
    _remove_artifacts: list[tuple[tuple[int, int],
                                  tuple[int, int]]] = []

    @staticmethod
    def _add_to_buffer(entity: Entity):

        # move cursor to position
        # terminal starts at 1,1
        Console._draw_buffer += f"\033[{entity.y_abs+1};{entity.x_abs+1}H"

        # set color
        Console._draw_buffer += Console.set_color(entity.display_rgb)

        Console._draw_buffer += str(entity)

    def _cleanup(self):
        self.show_cursor()
        self.clear_console()
        self.reset_format()

    @staticmethod
    def hide_cursor():
        print('\033[?25l', end="", flush=True)

    @staticmethod
    def show_cursor():
        print('\033[?25h', end="")

    @staticmethod
    def clear_console():
        match os.name:
            case "nt":
                os.system("cls")
            case "posix":
                os.system("clear")
            case _:
                print("\033[2J", end="", flush=True)

    @staticmethod
    def reset_format():
        print("\033[0m", end="")

    @staticmethod
    def set_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"
            pass

    def stop(self):
        self._stop_flag = True

    def run(self):
        self.clear_console()
        self.hide_cursor()
        try:
            asyncio.run(self._run_async())
            self._cleanup()
        except KeyboardInterrupt:
            self._cleanup()

    async def _run_async(self):

        children = self._collect_children()

        # start all animation loops
        for child in children:
            if isinstance(child, Animated):
                # _animation_loop() is protected
                asyncio.create_task(child._animation_loop())  # type: ignore

        # check for updates
        while self._stop_flag == False:
            await asyncio.sleep(1/100)  # one update per ms
            for child in children:
                if isinstance(child, Animated):
                    if child.draw_flag == True:
                        child.reset_drawflag()
                        child.draw_next()

                self._add_to_buffer(child)
            print(Console._draw_buffer, end="", flush=True)
            Console._draw_buffer = ""

            # lets user add custom functionality on runtime
            # checks for function update() in main file
            if callable(getattr(__main__, "update", None)):
                __main__.update()
