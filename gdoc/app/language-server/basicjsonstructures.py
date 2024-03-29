from typing import Any, Literal, TypeAlias, TypedDict, Union

########################################################
#
# Basic Types
#
########################################################

# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#uri
DocumentUri: TypeAlias = str


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentIdentifier
class TextDocumentIdentifier(TypedDict):
    uri: DocumentUri


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#versionedTextDocumentIdentifier
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentItem
class TextDocumentItem(TypedDict):
    uri: DocumentUri
    languageId: str
    version: int
    text: str


# Position in a text document expressed as zero-based line and zero-based character
# offset. A position is between two characters like an ‘insert’ cursor in an editor.
# Special values like for example -1 to denote the end of a line are not supported.
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#position
class Position(TypedDict):
    #  * Line position in a document (zero-based).
    # line: uinteger;
    line: int
    #  * Character offset on a line in a document (zero-based). The meaning of this
    #  * offset is determined by the negotiated `PositionEncodingKind`.
    #  *
    #  * If the character value is greater than the line length it defaults back
    #  * to the line length.
    # character: uinteger;
    character: int


# A range in a text document expressed as (zero-based) start and end positions. A range
# is comparable to a selection in an editor. Therefore, the end position is exclusive.
# If you want to specify a range that contains a line including the line ending
# character(s) then use an end position denoting the start of the next line.
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#range
class Range(TypedDict):
    #  * The range's start position.
    start: Position
    #  * The range's end position.
    end: Position


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#location
class Location(TypedDict):
    uri: DocumentUri
    range: Range


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#locationLink
class LocationLink_Option(TypedDict, total=False):
    #  * Span of the origin of this link.
    #  *
    #  * Used as the underlined span for mouse interaction. Defaults to the word
    #  * range at the mouse position.
    originSelectionRange: Range


class LocationLink(LocationLink_Option):
    #  * Span of the origin of this link.
    #  *
    #  * Used as the underlined span for mouse interaction. Defaults to the word
    #  * range at the mouse position.
    # originSelectionRange?: Range;

    #  * The target resource identifier of this link.
    targetUri: DocumentUri

    #  * The full target range of this link. If the target for example is a symbol
    #  * then target range is the range enclosing this symbol not including
    #  * leading/trailing whitespace but everything else like comments. This
    #  * information is typically used to highlight the range in the editor.
    targetRange: Range

    #  * The range that should be selected and revealed when this link is being
    #  * followed, e.g the name of a function. Must be contained by the
    #  * `targetRange`. See also `DocumentSymbol#range`
    targetSelectionRange: Range


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokens
class SemanticTokens_Option(TypedDict, total=False):
    #  * An optional result id. If provided and clients support delta updating
    #  * the client will include the result id in the next semantic token request.
    #  * A server can then instead of computing all semantic tokens again simply
    #  * send a delta.
    # resultId?: string;
    resultId: str


class SemanticTokens(SemanticTokens_Option):
    #  * The actual tokens.
    data: list[int]


#
# TextDocumentContentChangeEvent
#
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentContentChangeEvent
class TextDocumentContentChangeEvent_Full(TypedDict):
    #  * The new text of the whole document.
    # text: string;
    text: str


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentContentChangeEvent
class TextDocumentContentChangeEvent_Incremental_Option(TypedDict, total=False):
    # {
    #  * The range of the document that changed.
    # range: Range;
    #  * The optional length of the range that got replaced.
    #  * @deprecated use range instead.
    # rangeLength?: uinteger;
    rangeLength: int
    #  * The new text for the provided range.
    # text: string;


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentContentChangeEvent
class TextDocumentContentChangeEvent_Incremental(
    TextDocumentContentChangeEvent_Incremental_Option
):
    # {
    #  * The range of the document that changed.
    # range: Range;
    range: Any
    #  * The optional length of the range that got replaced.
    #  * @deprecated use range instead.
    # rangeLength?: uinteger;
    #  * The new text for the provided range.
    # text: string;
    text: str


TextDocumentContentChangeEvent: TypeAlias = Union[
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentContentChangeEvent
    TextDocumentContentChangeEvent_Full,
    TextDocumentContentChangeEvent_Incremental,
]


#
# MarkupContent
# A MarkupContent literal represents a string value which content can be represented in
# different formats. Currently plaintext and markdown are supported formats.
# A MarkupContent is usually used in documentation properties of result literals like
# CompletionItem or SignatureInformation. If the format is markdown the content should
# follow the GitHub Flavored Markdown Specification.
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#markupContent
class MarkupContent(TypedDict):
    #  * The type of the Markup
    kind: Literal["plaintext", "markdown"]  # MarkupKind type
    #  * The content itself
    value: str


########################################################
#
# Parameter Types
#
########################################################


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentPositionParams
class TextDocumentPositionParams(TypedDict):
    #  * The text document.
    textDocument: TextDocumentIdentifier
    #  * The position inside the text document.
    position: Position


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workDoneProgressParams
class WorkDoneProgressParams(TypedDict, total=False):
    #  * An optional token that a server can use to report work done progress.
    # workDoneToken?: ProgressToken;
    workDoneToken: int | str


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#partialResultParams
class PartialResultParams(TypedDict, total=False):
    #  * An optional token that a server can use to report partial results (e.g.
    #  * streaming) to the client.
    # partialResultToken?: ProgressToken;
    partialResultToken: int | str


class DidOpenTextDocumentParams(TypedDict):
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#didOpenTextDocumentParams
    #  * The document that was opened.
    textDocument: TextDocumentItem


class DidChangeTextDocumentParams(TypedDict):
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#didChangeTextDocumentParams
    #  * The document that did change. The version number points
    #  * to the version after all provided content changes have
    #  * been applied.
    textDocument: VersionedTextDocumentIdentifier
    #  * The actual content changes. The content changes describe single state
    #  * changes to the document. So if there are two content changes c1 (at
    #  * array index 0) and c2 (at array index 1) for a document in state S then
    #  * c1 moves the document from S to S' and c2 from S' to S''. So c1 is
    #  * computed on the state S and c2 is computed on the state S'.
    #  *
    #  * To mirror the content of a document using change events use the following
    #  * approach:
    #  * - start with the same initial content
    #  * - apply the 'textDocument/didChange' notifications in the order you
    #  *   receive them.
    #  * - apply the `TextDocumentContentChangeEvent`s in a single notification
    #  *   in the order you receive them.
    contentChanges: list[TextDocumentContentChangeEvent]


class DidSaveTextDocumentParams(TypedDict):
    #  * The document that was saved.
    textDocument: TextDocumentIdentifier
    #  * Optional the content when saved. Depends on the includeText value
    #  * when the save notification was requested.
    # text?: string;
    text: str


class DidCloseTextDocumentParams(TypedDict):
    # https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#didCloseTextDocumentParams
    #  * The document that was closed.
    textDocument: TextDocumentIdentifier


#
# Semantic Tokens
#
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokensParams
class SemanticTokensParams(WorkDoneProgressParams, PartialResultParams):
    #  * The text document.
    textDocument: TextDocumentIdentifier


#
# Goto Definition
#
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#definitionParams
class DefinitionParams(
    TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams
):
    pass


#
# Hover
#
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#hoverParams
class HoverParams(TextDocumentPositionParams, WorkDoneProgressParams):
    pass


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#markedString
class MarkedString_Language(TypedDict):
    # * The pair of a language and a value is an equivalent to markdown:
    # * ```${language}
    # * ${value
    # * ```
    #
    # * @deprecated use MarkupContent instead.
    #   ^^^^^^^^^^^
    language: str
    value: str


MarkedString: TypeAlias = str | MarkedString_Language


# The result of a hover request
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#hover
class Hover_Option(TypedDict, total=False):
    #  * An optional range is a range inside a text document
    #  * that is used to visualize a hover, e.g. by changing the background color.
    # range?: Range;
    range: Range


class Hover(Hover_Option):
    #  * The hover's content
    contents: MarkedString | list[MarkedString] | MarkupContent
