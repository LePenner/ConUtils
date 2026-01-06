from .commons import ObjDict, frame_type


class Mp_collector():
    def __init__(self, cores: int, frame: frame_type):
        self._mp_frame = frame
        self._mp_collect = self._mp_frame.copy()
        self._cores = cores

    def submit(self, obj: ObjDict, line_index: int):
        self._mp_collect[line_index].append(obj)
