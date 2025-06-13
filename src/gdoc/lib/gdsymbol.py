#
# path/to/file.md:ID.Id[name].id(tag,S,t:gd1002)
#


class Symbol:
    def __init__(self, symbol) -> None:
        pass

    @classmethod
    def isValid(cls, symbol):
        return True

    @classmethod
    def getFilePath(cls, symbol):
        parts = symbol.split(":")

        if len(parts) == 1:
            return None

        elif len(parts) == 2:
            return parts[0]

        else:
            # should raise.
            return None

    @classmethod
    def getId(cls, symbol):
        parts = symbol.split(":")

        if len(parts) <= 2:
            part = parts[-1]

        else:
            # should raise.
            return None

        parts = part.split("(")
        part = parts[0]

        if len(parts) == 2:
            if not parts[1].endswith(")"):
                # should raise.
                return None

        elif len(parts) > 2:
            # should raise.
            return None

        return part

    @classmethod
    def getTags(cls, symbol):
        tags = []
        parts = symbol.split("(")

        if len(parts) == 2:
            part = parts[1]
            if not part.endswith(")"):
                # should raise.
                return None

            tags = [x.strip() for x in part[:-1].split(",")]

        elif len(parts) > 2:
            # should raise.
            return None

        return tags

    @classmethod
    def isNameIncluded(cls, symbol):
        return True

    @classmethod
    def getParts(cls, symbol):
        parts = {"filePath": None, "symbol": [], "tag": []}

        return parts
