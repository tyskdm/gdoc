r"""
Document class
"""
from gdoc.lib.plugins.pluginmanager import PluginManager

from .baseobject import BaseObject


class Document(BaseObject):
    """ """

    def __init__(self, id, name=None, plugins: PluginManager | None = None):
        """ """
        super().__init__("DOCUMENT", id, name=name, plugins=plugins)
