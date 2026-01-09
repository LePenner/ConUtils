from .commons import ObjDict, frame_type, line_type, PreComp
from multiprocessing import Pool


class Mp_collector():
    def __init__(self, cores: int, frame: frame_type):
        self._mp_collect: frame_type = frame
        self._cores = cores

    def _mp_process(self, line: line_type):

        new_line = line.copy()
        for obj in line:
            PreComp.to_frame(obj, new_line)

        return new_line

    def submit(self, obj: ObjDict, line_index: int):
        self._mp_collect[line_index].append(obj)

    def process(self):
        with Pool(self._cores) as pool:
            self._mp_collect = pool.map(self._mp_process, self._mp_collect)
        return self._mp_collect
