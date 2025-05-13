from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.elements import Element
    from ..console import Console

obj_type = tuple[int, str, bool, bool, tuple[int, int, int] | None]
line_type = list[obj_type]
screen_type = list[line_type]


class Output:

    def __init__(self, console: Console):

        self.console = console
        self.clear()

    @staticmethod
    def get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @staticmethod
    def binsert_algo(x: int, lst: line_type) -> int:
        """Searches for index recursively."""

        piv = len(lst)//2

        if len(lst) > 0:

            # for normal usecases no overlap in representation positions
            # >>> no x == lst[piv][0]
            if x > lst[piv][0]:
                return piv+Output.binsert_algo(x, lst[piv+1:])+1
            else:
                return Output.binsert_algo(x, lst[:piv])
        else:
            return 0

    def clear(self):
        #             screen>line>obj(pos, rep, bold, italic, rgb(r,g,b)|None)
        self._screen: screen_type = [[] for _ in range(self.console.height)]

    def add(self, element: Element):
        """Add an Element to a line in screen.

        For every line of an elements representation, insert it into the right spot of the line.
        """

        for i, rep in enumerate(element.representation):

            line = element.y_abs+i
            index = self.binsert_algo(element.x_abs, self._screen[line])
            self._screen[line].insert(
                index, (element.x_abs, rep, element.bold, element.italic, element.display_rgb))

    def compile(self):
        out = ""
        for i, line in enumerate(self._screen):
            for j, obj in enumerate(line):
                if j > 0:
                    # addspacing
                    # starting position - starting position - len
                    out += " "*(obj[0] - line[j-1][0] - len(line[j-1][1]))
                else:
                    out += " "*obj[0]

                # add representation
                if obj[4]:
                    out += Output.get_color(obj[4])
                else:
                    out += "\033[0m"

                out += obj[1]

            if len(self._screen) != i+1:
                out += "\n"
            else:
                out += "\033[u"

        return out
