from __future__ import annotations
from typing import Unpack

from ..entity import Entity, EntityKwargs
from ..elements import Element
from ...errors import ethrow


class Container(Entity):
    """simple container class with child/parent logic"""

    def __init__(self,
                 overlap: bool = False, **kwargs: Unpack[EntityKwargs]):

        self._children: list[Entity] = []
        self._overlap = overlap
        super().__init__(**kwargs)

    def _set_display_rgb(self, rgb: tuple[int, int, int] | None = None):

        # initialisation and failsafe if no parrent
        if rgb:
            self._display_rgb = rgb
        else:
            self._display_rgb = self.rgb

        if self.parent and not self.rgb:
            self._display_rgb = self.parent.display_rgb
            for child in self.children:
                child._display_rgb = child._get_display_rgb()
        else:
            for child in self.children:
                child._display_rgb = child._get_display_rgb()
            return self.rgb

    # ----- make dimension setter public -----

    @Entity.width.setter
    def width(self, width: int) -> int | None:
        if self.parent and hasattr(self, 'x'):
            if self.parent.width < self.x + width:
                ethrow("ENTY", "edge conflict")
        self._width = width
        self._overlap_check()

    @Entity.height.setter
    def height(self, height: int) -> int | None:
        if self.parent and hasattr(self, 'y'):
            if self.parent.height < self.y + height:
                ethrow("ENTY", "edge conflict")
        self._height = height
        self._overlap_check()

    @Entity.dimensions.setter
    def dimensions(self, cords: tuple[int, int]):
        self._width = cords[0]
        self._height = cords[1]

    # ----- properties -----

    @property
    def children(self) -> list[Entity]:
        return self._children

    @property
    def overlap(self) -> bool:
        return self._overlap

    # ----- child logic -----

    def _collect_children(self) -> list[Element]:
        result: list[Element] = []

        for child in self._children:
            if isinstance(child, Container):
                result.extend(child._collect_children())
            else:
                if isinstance(child, Element):
                    result.append(child)
        return result

    def add_child(self, child: Entity, replace: bool = False):
        self._overlap_check()
        if child._parent and not replace:
            ethrow("ENTY", "parent double")
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: Entity):
        if child not in self._children:
            ethrow("ETNY", "child not found")
        self._children.remove(child)
        child._parent = None

    # ----- parent logic -----

    def set_parent(self, parent: Container | None = None, replace: bool = False):
        if parent in self._children and not replace:
            ethrow("ENTY", "incest")

        if parent in self._children:
            self._children.remove(parent)
        if parent:
            if parent._parent == self:
                parent._parent = None
            self._parent = parent
            parent._children.append(self)
