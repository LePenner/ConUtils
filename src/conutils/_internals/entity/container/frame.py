from __future__ import annotations
from typing import TYPE_CHECKING

from conutils._internals.errors.errors import ethrow

if TYPE_CHECKING:
    from .container import Container

from typing import Unpack
from conutils._internals.entity.entity import EntityKwargs
from ...errors import ethrow
from ...entity import Entity


class Frame(Entity):
    def __init__(self,
                 vert_edge: str = "|",
                 hori_edge: str = "=",
                 corner: str = "#",
                 **kwargs: Unpack[EntityKwargs]):

        self.vertical_edge = vert_edge
        self.horrizontal_edge = hori_edge
        self.corner = corner

        self.container = kwargs.get("parent")

        super().__init__(**kwargs)

    @property
    def container(self):
        return self.parent

    @container.setter
    def container(self, container: Container | None):
        if container:
            self.parent = container
            self.presentation()
        else:
            self.parent = None

    @property
    def pos(self) -> tuple[int, int]:
        ethrow("FRAM", "read from Frame")

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        ethrow("FRAM", "read from Frame")

    @property
    def width(self) -> int:
        ethrow("FRAM", "read from Frame")

    @property
    def height(self) -> int:
        ethrow("FRAM", "read from Frame")

    def presentation(self):
        """Process presentation settings.

        Can only be called if a container/parent is set."""
        if not self.parent:
            raise Exception

        if self.parent.width < len(self.corner)*2:
