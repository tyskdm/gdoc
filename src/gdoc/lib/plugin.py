# Gdoc object types

from ..plugin import sysml


class Plugins:
    def __init__(self, pluginpath=None) -> None:
        self.typetable = _TypeTable
        self.typetable["sysml"] = sysml.exports
        pass

    # self, block.type, tag.plugin, tag.types
    def getConstructor(self, package, blocktype, plugin, types):
        constructor = None
        if plugin is None:
            plugin = ""
            pkg = package
            while pkg is not None:
                if pkg.plugin is not None:
                    plugin = pkg.plugin
                    if self.typetable.get(plugin.lower()) is None:
                        return "ERROR: Unknown plugin"

                    elif self.typetable[plugin.lower()].get(blocktype) is None:
                        return (
                            "ERROR: Plugin("
                            + plugin
                            + ') does not provide types for "'
                            + blocktype
                            + '"'
                        )

                    typeinfo = self.typetable[plugin.lower()][blocktype].get(
                        ".".join(types).lower()
                    )
                    if typeinfo is None:
                        pkg = pkg.parent
                        continue
                    else:
                        constructor = typeinfo["constructor"]
                        break

                pkg = pkg.parent

        else:
            typeinfo = self.typetable[plugin.lower()][blocktype].get(
                ".".join(types).lower()
            )
            constructor = typeinfo["constructor"]

        return constructor


_TypeTable = {
    "": {"Para": {"import": {"constructor": None}, "access": {"constructor": None}}}
}
