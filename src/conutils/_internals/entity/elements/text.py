from __future__ import annotations
from typing import Unpack

from ..entity import EntityKwargs
from ...errors import ethrow
from .element import Element


class Text(Element):
    def __init__(self,
                 representation: list[str] | str | None = None,
                 **kwargs: Unpack[EntityKwargs]):
        """Representation in format ["First Line","Second Line", "Third Line"] or as string with '\\n'.
        """

        self._str = ""
        self._repr = self._get_proper_repr(representation)

        dimension: tuple[int, int] = self._get_dimensions(self._repr)
        kwargs["width"] = dimension[0]
        kwargs["height"] = dimension[1]

        super().__init__(**kwargs)

    def _get_proper_repr(self, representation: str | list[str] | None):

        repr = []

        # convert multi line string into printable format
        if isinstance(representation, str):
            try:
                repr = [
                    representation.strip("\n") for representation in representation.split("\n")]
            except:
                ethrow("TEXT", "faulty string")
        elif representation != None:
            repr = representation

        return repr

    def _get_dimensions(self, representation: str | list[str] | None):

        # convert multi line string into printable format
        self._repr = self._get_proper_repr(representation)

        if self._repr:
            width = 0
            for line in self._repr:
                if not line.isprintable():
                    ethrow("TEXT", "faulty string")

                if len(line) > width:
                    width = len(line)
            height = len(self._repr)
        else:
            width = 1
            height = 1

        return (width, height)

    @property
    def representation(self):
        return self._repr

    @representation.setter
    def representation(self, representation: str | list[str] | None):

        self._repr = self._get_proper_repr(representation)
        self._dimension = self._get_dimensions(representation)
