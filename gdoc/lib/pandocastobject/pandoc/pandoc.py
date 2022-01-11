r"""
Pandoc class
"""
import subprocess

class Pandoc:
    """
    Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.
    """

    def __init__(self):
        """ Constructor
        """
        self._version = None
        self._version_str = None


    def _run(self, commandlines, stdin=None):
        """ run multiple subcommands
        run multiple subcommands while connecting it with pipes and return the output.
        @param comandlines([Str])
            Commandline strings including options to run as subprocesses.
        @param stdin
            stdin port passed to the first subcommand.
        @return output : Str
            stdout from the last subcommand.
        """
        output = None
        args = commandlines[0].split()

        with subprocess.Popen(args, stdin=stdin,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) as ps:

            if len(commandlines) > 1:
                output = self._run(commandlines[1:], stdin=ps.stdout)
                ps.wait()

            else:
                ps.wait()
                output = b''.join(ps.stdout.readlines())

            if ps.returncode != 0:
                # subprocess.check_output():
                # https://docs.python.org/3/library/subprocess.html#subprocess.check_output
                # > If the return code was non-zero it raises a CalledProcessError.
                raise subprocess.CalledProcessError(
                    ps.returncode, args,
                    b''.join(ps.stdout.readlines()),
                    b''.join(ps.stderr.readlines())
                )

        return output


    def get_json(self, filepath, fromType=None):
        """
        """
        commands = []

        if fromType is None:
            if (filepath.split('.')[-1]) == 'md':
                cmd = 'pandoc -f gfm+sourcepos -t html'
                cmd += ' ' + filepath
                commands.append(cmd)

                cmd = 'pandoc -f html -t json'
                commands.append(cmd)

            else:
                cmd = 'pandoc -t json'
                cmd += ' ' + filepath
                commands.append(cmd)

        else:
            cmd = 'pandoc -t json'
            cmd += ' -f ' + fromType
            cmd += ' ' + filepath
            commands.append(cmd)

        return self.run(commands)


    def get_version(self):
        """
        """

        output = self.run(['pandoc --version'])
