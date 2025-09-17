# This code is a modified version of:
# https://github.com/palantir/python-jsonrpc-server/blob/develop/pyls_jsonrpc/streams.py
import json
import logging
import threading
from typing import BinaryIO, Dict, List, Union

logger = logging.getLogger(__name__)

JSONPrimitive = Union[str, int, float, bool, None]
JSONType = Union[JSONPrimitive, List["JSONType"], Dict[str, "JSONType"]]


class JsonStream:
    def __init__(self, rfile: BinaryIO, wfile: BinaryIO, **json_dumps_args):
        self._rfile = rfile
        self._wfile = wfile
        self._wfile_lock = threading.Lock()
        self._json_dumps_args = json_dumps_args

    def close(self):
        self._rfile.close()
        with self._wfile_lock:
            self._wfile.close()

    def write(self, message: JSONType):
        content: bytes = json.dumps(message, **self._json_dumps_args).encode("utf-8")
        content_length: int = len(content)
        data_frame: bytes = (
            b"Content-Length: "
            + str(content_length).encode("utf-8")
            + b"\r\n"
            + b"Content-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n"
            + content
        )
        with self._wfile_lock:
            if self._wfile.closed:
                return

            try:
                self._wfile.write(data_frame)
                self._wfile.flush()
            except Exception:  # pylint: disable=broad-except
                logger.exception("Failed to write message to output file %s", message)

    def read(self) -> JSONType | None:
        msg: bytes | None = self.read_message()
        return json.loads(msg.decode("utf-8")) if msg else None

    def read_message(self) -> bytes | None:
        """Reads the contents of a message.

        Returns:
            body of message if parsable else None
        """
        line: bytes = self._rfile.readline()

        if line == b"":
            return None  # EOF

        content_length = self._content_length(line)
        if content_length is None:
            return None  # the line is not Content-Length header

        # Blindly consume all header lines
        while line.strip():
            line = self._rfile.readline()

        if line == b"":
            return None  # EOF

        # Grab the body
        return self._rfile.read(content_length)

    @staticmethod
    def _content_length(line: bytes) -> int | None:
        """Extract the content length from an input line."""
        if line.startswith(b"Content-Length: "):
            _, value = line.split(b"Content-Length: ", 1)
            value = value.strip()
            try:
                return int(value)
            except ValueError:
                raise ValueError("Invalid Content-Length header: {}".format(value))

        return None
