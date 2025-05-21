from __future__ import annotations
from typing import Unpack

from ..entity import EntityKwargs
from .element import Element


class StaticText(Element):
    def __init__(self, representation: list[str] | str | None = None, **kwargs: Unpack[EntityKwargs]):
        """representation in format ["First Line","Second Line", "Third Line"]"""
        self._str = ""

        # convert multi line string into printable format
        if type(representation) == str:
            try:
                representation = [
                    representation.strip("\n") for representation in representation.split("\n")]
            except:
                raise Exception()

        if type(representation) == list:
            self._repr = representation
        elif type(representation) == str:
            self._repr = [representation]
        else:
            self._repr = []

        kwargs["width"] = 0

        if representation:

            for l in representation:
                if not l.isprintable():
                    raise Exception()
                if self._str == "":
                    self._str = l
                else:
                    self._str += '\n\033[{x}{direction}'+l

                if len(l) > kwargs["width"]:
                    kwargs["width"] = len(l)
            kwargs["height"] = len(representation)
        else:
            kwargs["width"] = 1
            kwargs["height"] = 1

        super().__init__(**kwargs)

    def __str__(self):
        # for right indentation on every line
        if self.x_abs > 0:
            return self._str.format(x=self.x_abs, direction="C")
        else:
            return self._str.format(x=self.x_abs, direction="D")

    @property
    def representation(self):
        return self._repr
