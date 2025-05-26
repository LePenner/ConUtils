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
        self.representation = representation

        super().__init__(**kwargs)

    @property
    def representation(self):
        return self._repr

    @representation.setter
    def representation(self, representation: str | list[str] | None):

        # convert multi line string into printable format
        if isinstance(representation, str):
            try:
                self._repr = [
                    representation.strip("\n") for representation in representation.split("\n")]
            except:
                ethrow("TEXT", "faulty string")
        elif representation != None:
            self._repr = representation
        else:
            self._repr = []

        if representation:
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

        self._dimension = (width, height)
