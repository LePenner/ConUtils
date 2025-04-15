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
from ._internals import Colors
from ._internals.entity.elements import Spinner, StaticText
from ._internals.entity.container import Container

__all__ = ["Container", "Spinner", "StaticText", "Console", "Colors"]
