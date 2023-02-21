"""
datapos.py: DataPos class
"""
from gdoc.lib.pandocastobject.pandocast import DataPos as PandocDataPos
from gdoc.lib.pandocastobject.pandocast import Pos as PandocPos


class Pos(PandocPos):
    pass


class DataPos(PandocDataPos):
    def dumpd(self):
        return [self.path, self.start.ln, self.start.col, self.stop.ln, self.stop.col]

    @classmethod
    def loadd(cls, data: list):
        return DataPos(data[0], Pos(data[1], data[2]), Pos(data[3], data[4]))
