r"""
GdSymbol class
"""
import re

from gdoc.lib.gdoccompiler.gdexception import GdocSyntaxError


class GdSymbol:
    """
    ;
    """

    IS_NAME_STR = "@"
    # "@" is a character not allowed in id.
    # Set it at the beginning of a string to indicate that
    # the string is not an id, i.e., a name.

    def __init__(self, symbol):
        """ """
        self.__symbols, self.__tags = GdSymbol._split_symbol(symbol)
        self.__symbol_str = symbol  # str is immutable and needless to copy.
        # TODO: PandocStr needs to copy.

    def is_id(self):
        """ """
        return not self.__symbols[-1].startswith(GdSymbol.IS_NAME_STR)

    def get_symbols(self):
        """ """
        return self.__symbols[:]

    def get_symbol_str(self):
        """ """
        symbol_str = ""

        for s in self.__symbols:
            if s.startswith(GdSymbol.IS_NAME_STR):
                symbol_str += "[" + s[1:] + "]"
            elif symbol_str != "":
                symbol_str += "." + s
            else:
                symbol_str = s

        return symbol_str

    def get_tags(self):
        """ """
        return self.__tags[:]

    #
    # Class Methods
    #
    @classmethod
    def is_valid_symbol(cls, symbol):
        """ """
        result = True

        try:
            cls._split_symbol(symbol)
        except:
            result = False

        return result

    @classmethod
    def is_valid_id(cls, symbol):
        """ """
        result = GdSymbol._is_gdoc_identifier(symbol)

        if result is not True:
            result = False

        return result

    #
    # Class Private Variables and Methods
    #
    _IDENTIFIER = re.compile(r"\.(\S*?)(?=(\.|\[|\(|$))")
    _IDENTIFIER_INDEX = 1

    _TAG_STRING = re.compile(r"\((.*)\)$")
    _TAG_STRING_INDEX = 1
    _TAG_DELIMITER = re.compile(r"\s*,\s*|\s+")
    _TAG_INVALID_SYNTAX = re.compile(r"\(\s*,|,\s*[,)]")

    @classmethod
    def _split_symbol(cls, symbolstr: str):
        """split symbol string to ids or names and tags.
        @param symbol : str | PandocStr
        @return (list(str), list(str))

        T.B.D. : Error handling
        """
        symbol = symbolstr.strip()
        column = symbolstr.index(symbol) + 1  # Column is starting from 1.

        if not symbol.startswith(("[", "(")):
            target = "." + symbol
            column -= 1
        else:
            target = symbol

        symbols = []
        tags = []
        while len(target) > 0:
            if target.startswith("["):
                try:
                    name, length = cls._get_namestr(target)
                except GdocSyntaxError as err:
                    raise GdocSyntaxError(
                        err.msg, (None, None, column + err.offset, str(symbolstr))
                    ) from err

                if name.startswith('"'):
                    name = name[1:-1]
                else:
                    if (i := cls._is_gdoc_identifier(name)) is not True:
                        raise GdocSyntaxError(
                            "invalid character in non-quoted name",
                            (None, None, column + i + 1, str(symbolstr))
                            # column + i + len('[')
                        )

                symbols.append(GdSymbol.IS_NAME_STR + name)

            elif s := cls._IDENTIFIER.match(target):
                identifier = s.group(cls._IDENTIFIER_INDEX)
                length = len(s.group(0))

                if identifier == "":
                    column = column + length
                    if column > len(symbolstr):
                        # in case _IDENTIFIER matched with $(EOL)
                        column -= 1

                    raise GdocSyntaxError(
                        "invalid syntax", (None, None, column, str(symbolstr))
                    )
                elif (i := cls._is_gdoc_identifier(identifier)) is not True:
                    raise GdocSyntaxError(
                        "invalid character in identifier",
                        (None, None, column + i + 1, str(symbolstr))
                        # column + i + len('.')
                    )

                symbols.append(identifier)

            elif s := cls._TAG_STRING.match(target):
                tags = s.group(cls._TAG_STRING_INDEX).strip()
                length = len(s.group(0))

                if len(tags) > 0:
                    tags = cls._TAG_DELIMITER.split(tags)
                else:
                    tags = []

                for tag in tags:
                    if tag != "":
                        hash_added = 1 if tag.startswith("#") else 0
                        if (i := cls._is_gdoc_identifier(tag[hash_added:])) is not True:
                            i += target.index(tag) + hash_added
                            raise GdocSyntaxError(
                                "invalid character in tag",
                                (None, None, column + i, str(symbolstr)),
                            )
                    else:  # tag == ""
                        m = cls._TAG_INVALID_SYNTAX.search(target)
                        raise GdocSyntaxError(
                            "invalid syntax",
                            (None, None, column + m.end() - 1, str(symbolstr)),
                        )

            else:
                raise GdocSyntaxError(
                    "invalid syntax", (None, None, column, str(symbolstr))
                )

            column += length
            target = target[length:]

        return symbols, tags

    @classmethod
    def _is_gdoc_identifier(cls, identifier):
        result = False

        if ("a" + identifier).isidentifier():
            result = True

        else:
            for c in identifier:  # pragma: no branch: This line never complete.
                if not ("a" + c).isidentifier():
                    break

            result = identifier.index(c)

        return result

    @classmethod
    def _get_namestr(cls, target):
        name = ""
        index = 1  # skip the top '['
        length = len(target)

        #
        # Skip leading white spaces
        #
        while index < length and target[index] == " ":
            index += 1

        if index == length:
            raise GdocSyntaxError(
                "EOS while scanning name string", (None, None, index - 1, target)
            )

        #
        # Quoted string
        #
        if target[index] == '"':
            name += '"'
            index += 1

            while index < length:
                c = target[index]

                if c == '"':  # Wait closing '"'
                    name += c
                    index += 1
                    break

                if c == "\\":  # Escape sequence
                    index += 1
                    if index == length:
                        break

                    c = target[index]
                    if c == '"':
                        name += '"'
                    elif c == "\\":
                        name += "\\"
                    else:
                        name += "\\" + c

                else:
                    name += c

                index += 1

            if index == length:  # String not close
                raise GdocSyntaxError(
                    "EOS while scanning string literal", (None, None, index - 1, target)
                )

        #
        # invalid syntax
        #
        elif target[index] == "]":
            raise GdocSyntaxError("invalid syntax", (None, None, index, target))

        #
        # Non-quoted string
        #
        else:
            while index < length and (c := target[index]) != "]":

                if c == " ":  # string ended
                    break

                else:
                    name += c

                index += 1

        #
        # Wait closing ']'
        #
        while index < length:
            if target[index] == "]":
                break

            elif target[index] != " ":
                raise GdocSyntaxError("invalid syntax", (None, None, index, target))

            # else: target[i] == ' '
            index += 1

        if index == length:
            raise GdocSyntaxError(
                "EOS while scanning name string", (None, None, index - 1, target)
            )

        name = name.rstrip()

        return name, index + 1
