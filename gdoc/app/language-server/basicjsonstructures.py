from typing import Any, TypeAlias, TypedDict, Union


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentIdentifier
class TextDocumentIdentifier(TypedDict):
    uri: str


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#versionedTextDocumentIdentifier
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    version: int


# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocumentItem
class TextDocumentItem(TypedDict):
    uri: str
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
