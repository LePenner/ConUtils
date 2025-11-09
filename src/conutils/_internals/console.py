import __main__
import os
import asyncio
import time
from multiprocessing import cpu_count, freeze_support, current_process
from typing import Unpack
from .entity.elements import Element
from .entity.container import Container
from .toolkit.screen_compiler import Output
from .entity.entity import EntityKwargs
from .errors import ethrow


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal.

    define an `update` function to configure runtime behavior.
    """

    _instance = None

    def __init__(self,
                 overlap: bool = False,
                 fps: int = 0,
                 multiprocessing: bool | int = False,
                 **kwargs: Unpack[EntityKwargs]):
        self._stop_flag = False
        self.fps = fps

        if multiprocessing == True:
            multiprocessing = cpu_count()
        elif multiprocessing != False:
            if multiprocessing > cpu_count():
                ethrow("CONS", "too many processes")

        self._processes = multiprocessing

        # set default length and height to terminal
        kwargs["width"] = kwargs.get("width") or\
            os.get_terminal_size()[0]
        kwargs["height"] = kwargs.get("height") or\
            os.get_terminal_size()[1]

        super().__init__(overlap=overlap, **kwargs)

    def _cleanup(self):

        if self._otp.pool:
            self._otp.pool.terminate()

        self.show_cursor()
        self.clear_console()
        self.reset_format()

    @staticmethod
    def hide_cursor():
        print('\033[?25l', end="")

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
                print("\033[H\033[J", end="")

    @staticmethod
    def reset_format():
        print("\033[0m", end="")

    def stop(self):
        self._stop_flag = True

    def run(self):

        freeze_support()
        if current_process().name != "MainProcess":
            return

        self._otp = Output(self, self._processes)
        self.clear_console()
        self.hide_cursor()

        try:
            self._run_async()
            self._cleanup()
        except KeyboardInterrupt:
            self._cleanup()

    def _run_async(self):

        children = self._collect_children()

        # start all animation loops
        for child in children:
            if hasattr(child, "_animation_loop"):
                # _animation_loop() is protected
                asyncio.create_task(child._animation_loop())  # type: ignore

        # avg error of about -0.5 ms
        def tick_generator():
            t = time.perf_counter()
            while True:
                t += 1/self.fps
                yield max(t - time.perf_counter(), 0)
        tick = tick_generator()

        while self._stop_flag == False:

            # lets user add custom functionality on runtime
            # checks for function update() in main file
            if getattr(__main__, "update", None):
                __main__.update()  # type:  ignore

            if self.fps:
                self.calc(children)
                time.sleep(next(tick))
            else:
                self.calc(children)

    def calc(self, children: list[Element]):
        if self._processes:
            self._otp.start_processor()

        for child in children:
            self._otp.add(child)
        self._otp.stop_processor = True

        print(self._otp.compile(), end="\r")
        self._otp.clear()
