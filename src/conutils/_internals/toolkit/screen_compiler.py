from __future__ import annotations
from typing import TYPE_CHECKING

from conutils._internals.console import Console

if TYPE_CHECKING:
    from ..entity.elements import Element
    from ..console import Console

obj_type = tuple[int, str, bool, bool, tuple[int, int, int] | None]
line_type = list[obj_type]
screen_type = list[line_type]


class Output:

    def __init__(self, console: Console):

        #             screen>line>obj(pos, rep, bold, italic, rgb(r,g,b)|None)
        self.screen: screen_type = [[] for _ in range(console.height)]

    # keep track of ansi esc seq length

    def add(self, element: Element):
        """Add an Element to a line in screen.

        For every line of an elements representation, insert it into the right spot of the line.
        """

        for i, rep in enumerate(element.representation):

            line = element.y_abs+i
            index = self.binsert_algo(element.x_abs, self.screen[line])
            self.screen[line].insert(
                index, (element.x_abs, rep, element.bold, element.italic, element.display_rgb))

    @staticmethod
    def binsert_algo(x: int, lst: line_type) -> int:
        """Searches for index recursively."""

        piv = len(lst)//2

        if len(lst) > 1:

            if x > lst[piv][0]:
                return piv+Output.binsert_algo(x, lst[piv+1:])
            elif x == lst[piv][0]:
                raise 
            else:
                return Output.binsert_algo(x, lst[:piv])
        elif len(lst) == 1:
            return 1
        else:
            return 0
