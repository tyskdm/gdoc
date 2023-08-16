# This code is a modified version of:
# https://github.com/palantir/python-jsonrpc-server/blob/develop/pyls_jsonrpc/streams.py
import json
import logging
import sys
import threading

logger = logging.getLogger(__name__)


class JsonStream:
    def __init__(self, rfile, wfile, **json_dumps_args):
        self._rfile = sys.stdin.buffer if rfile is sys.stdin else rfile
        self._wfile = wfile
        self._wfile_lock = threading.Lock()
        self._json_dumps_args = json_dumps_args

    def close(self):
        self._rfile.close()
        with self._wfile_lock:
            self._wfile.close()

    def write(self, message):
        with self._wfile_lock:
            if self._wfile.closed:
                return
            try:
                body = json.dumps(message, **self._json_dumps_args)

                # Ensure we get the byte length, not the character length
                content_length = (
                    len(body) if isinstance(body, bytes) else len(body.encode("utf-8"))
                )

                response = (
                    "Content-Length: {}\r\n"
                    "Content-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n"
                    "{}".format(content_length, body)
                )

                self._wfile.write(response)
                self._wfile.flush()
            except Exception:  # pylint: disable=broad-except
                logger.exception("Failed to write message to output file %s", message)

    def read(self):
        msg = self.read_message()
        return json.loads(msg.decode("utf-8")) if msg else None

    def read_message(self) -> bytes | None:
        """Reads the contents of a message.

        Returns:
            body of message if parsable else None
        """
        line: str = self._rfile.readline()

        if not line:
            return None

        content_length = self._content_length(line)

        # Blindly consume all header lines
        while line and line.strip():
            line = self._rfile.readline()

        if not line:
            return None

        # Grab the body
        return self._rfile.read(content_length)

    @staticmethod
    def _content_length(line):
        """Extract the content length from an input line."""
        if line.startswith(b"Content-Length: "):
            _, value = line.split(b"Content-Length: ")
            value = value.strip()
            try:
                return int(value)
            except ValueError:
                raise ValueError("Invalid Content-Length header: {}".format(value))

        return None
