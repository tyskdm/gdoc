r"""
Gdoc Exception Classes
"""


class GdocIdError(KeyError):
    pass


class GdocKeyError(KeyError):
    pass


class GdocImportError(ImportError):
    pass


class GdocModuleNotFoundError(ModuleNotFoundError):
    pass


class GdocNameError(NameError):
    pass


class GdocRuntimeError(RuntimeError):
    pass


class GdocSyntaxError(SyntaxError):
    pass


class GdocTypeError(TypeError):
    pass
