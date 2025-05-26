# conutils/

"""ConUtils API.

`Console`, `Screen` and `Line` are all `Containers` to structure your console output.
`Console` is the main screen and handles drawing `Elements`, add containers or `Elements`
like `Spinner` and `Text` as children, to display them.

@Exposes
    classes
        - :class:`Console`
        - :class:`Spinner`
        - :class:`Text`
        - :class:`Container`
"""

# pulls API components diretly
from ._internals import Console
from ._internals.toolkit import Color
from ._internals.entity.elements import Spinner, Text, Log
from ._internals.entity.container import Container

LOGO = """
  ,ad8888ba,
 d8"'    `"8b
d8'
88    88        88
Y8,   88        88
 Y8a. 88 .a8P   88
  `"Y8888Y"'    88
      88        88
      Y8a.    .a8P
       `"Y8888Y"'
"""

__all__ = ["Container", "Spinner", "Text",
           "Log", "Console", "Color", "LOGO"]
