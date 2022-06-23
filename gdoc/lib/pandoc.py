import logging
import subprocess

_LOGGER = logging.getLogger(__name__)


class Pandoc:
    def __init__(self) -> None:
        pass

    def run(self, file, fromType=None):
        commands = []

        if fromType is None:
            if (file.split(".")[-1]) == "md":
                cmd = "pandoc -f gfm+sourcepos -t html".split()
                cmd.append(file)
                commands.append(cmd)

                cmd = "pandoc -f html -t json".split()
                commands.append(cmd)

            else:
                cmd = "pandoc -t json".split()
                cmd.append(file)
                commands.append(cmd)

        else:
            cmd = "pandoc -t json -f".split()
            cmd.append(fromType)
            cmd.append(file)
            commands.append(cmd)

        output = None
        procs = []
        with subprocess.Popen(commands[0], stdout=subprocess.PIPE) as ps:
            procs.append(ps)

            if len(commands) > 1:
                with subprocess.Popen(
                    commands[1], stdin=procs[0].stdout, stdout=subprocess.PIPE
                ) as ps:
                    procs.append(ps)
                    output = procs[-1].communicate()[0]
                    procs[0].communicate()
                    if (procs[0].returncode != 0) or (procs[1].returncode != 0):
                        # should raise
                        output = None

            else:
                output = procs[-1].communicate()[0]
                if procs[0].returncode != 0:
                    # should raise
                    output = None

        return output
