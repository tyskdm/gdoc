"""
datapos.py: DataPos class
"""
from gdoc.lib.pandocastobject.pandocast import DataPos as PandocDataPos
from gdoc.lib.pandocastobject.pandocast import Pos as PandocPos


class Pos(PandocPos):
    pass


class DataPos(PandocDataPos):
    def dumpd(self) -> list:
        return [self.path, self.start.ln, self.start.col, self.stop.ln, self.stop.col]

    @classmethod
    def loadd(cls, data: list) -> "DataPos":
        return DataPos(data[0], Pos(data[1], data[2]), Pos(data[3], data[4]))

    def get_last_pos(self) -> "DataPos":
        start: Pos
        if (self.stop.ln > 0) and (self.stop.col > 0):
            start = Pos(self.stop.ln, self.stop.col)
        else:
            start = Pos(self.start.ln, self.start.col)

        return DataPos(self.path, start, Pos(0, 0))

    def extend(self, other: "DataPos") -> "DataPos":
        return DataPos(
            self.path,
            self.start,
            other.stop if (other.stop.ln > 0) else other.start,
        )
