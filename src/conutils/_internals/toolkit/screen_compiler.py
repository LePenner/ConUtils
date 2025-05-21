from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.elements import Element
    from ..console import Console

#             screen>line>obj(pos, rep, bold, italic, rgb(r,g,b)|None)
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
            # fill line with spaces if empty
            if len(line) == 0:
                out += " "*self.console.width

            for j, obj in enumerate(line):
                if j > 0:
                    # add spacing
                    # starting position - starting position - len(obj)
                    out += " "*(obj[0] - line[j-1][0] - len(line[j-1][1]))
                else:
                    out += " "*obj[0]

                # check for color
                if obj[4]:
                    out += Output.get_color(obj[4])
                else:
                    # reset color
                    out += "\033[39m"

                # add representation
                out += obj[1]

                # if last object in line:
                if len(line) == j+1:
                    # fill rest of line with spaces
                    out += " "*(self.console.width - obj[0] - len(obj[1]))

            # add new line at end of line
            if len(self._screen) != i+1:
                out += "\n"
            # if last line: return to top left
            else:
                out += "\033[u"
        return out
