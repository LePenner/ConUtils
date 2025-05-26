from datetime import datetime

from typing import Callable, Unpack
from conutils._internals.entity import EntityKwargs
from .element import Element

# add max length


class Log(Element):
    def __init__(self,
                 display_time: int = 10,
                 layout: str = "[{timestamp}][{status}] {msg}",
                 status: str = "running",
                 msg: str = "",
                 max_width: int = 0,
                 ** kwargs: Unpack[EntityKwargs]
                 ):
        """Log also creates a log file.

        Defineable parameters: `timestamp, `status` and `msg` per default,
        can be expanded on.
        """

        self._values: dict[str, str | Callable[[], str]] = {
            "timestamp": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status.upper(),
            "msg": msg
        }

        self._display_time = display_time
        self._layout = layout
        self.max_width = max_width
        self.log(msg)
        if max_width:
            kwargs["width"] = max_width
        else:
            kwargs["width"] = len(self.__initial_repr()[0])

        super().__init__(**kwargs)

    def __initial_repr(self):
        values = {
            key: val() if callable(val) else val
            for key, val in self._values.items()
        }

        otp = self._layout.format(**values)
        self._dimension = (len(otp), 1)
        return [otp]

    @property
    def representation(self):

        values = {
            key: val() if callable(val) else val
            for key, val in self._values.items()
        }

        otp = self._layout.format(**values)

        if self.max_width:
            if len(otp) > self.max_width:
                return [otp[:self.max_width-3:]+"..."]
            return [otp]

        self._dimension = (len(otp), 1)
        self._overlap_check()
        return [otp]

    def add_value(self, key: str, val: str | Callable[[], str], replace: bool = False):
        if not key in self._values or replace:
            self._values[key] = val
        else:
            raise Exception  # --------------- make proper exception

    def log(self, msg: str, display: bool = True):
        if display == True:
            self._values["msg"] = msg

        with open("log.txt", "a") as f:
            f.write(
                f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{self._values["status"]}] {msg}" + "\n")
