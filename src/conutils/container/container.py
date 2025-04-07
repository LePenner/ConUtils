class Container():
    def __init__(self, x=0, y=0, parent=None):
        self.parent=parent
        self.children=[]

        self._x = self.set_x(x)
        self._y = self.set_y(y)

        if parent:
            parent.add_child(self)

    def set_x(self, x):
        self._x = self.parent._x + x

    def set_y(self, y):
        self._y = self.parent._y + y
    
    def add_child(self, child, replace=False):
        if child.parrent and not replace:
            raise StructureError('parent double')
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

class StructureError(Exception):
    def __init__(self, key):
        messages = { 'parent double'  : "specified child already has parent associated, try 'replace=True'",
                    }

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'invalid structure\n  ' + message)