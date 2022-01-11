r"""
The specification of Pandoc class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/Pandoc]

### THE TARGET

[@import SWDD.SU[Pandoc] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Pandoc       | Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.
| @Method | \_\_init\_\_ | creates a new instance.
| @Method | \_run        | run multiple subcommands while connecting it with pipes and return the output.

"""
import pytest
import inspect
from subprocess import PIPE as _PIPE_
from subprocess import CalledProcessError
from gdoc.lib.pandocastobject.pandoc.pandoc import Pandoc

## @{ @name \_\_init\_\_(self)
## [\@spec \_\_init\_\_] creates a new instance.
##
___init__ = "dummy for doxygen styling"

def spec___init___1():
    r"""
    [@spec \_\_init\_\_.1] `Element` should be a class.
    """
    assert inspect.isclass(Pandoc) == True

def spec___init___2():
    r"""
    [@spec \_\_init\_\_.2] set props with default values.
    """
    target = Pandoc()

    assert target._version == None
    assert target._version_str == None


## @}
## @{ @name _run(self, commandlines, stdin=None)
## [\@spec _run] run multiple subcommands while connecting it with pipes and return the output.
##

_data__run_1 = {
#   id: (
#       commandlines,
#       popen: [(returncode, b'stdout', b'stderr')],
#       expected: {
#           output,
#           popen: {
#               call_count, args
#           },
#           communicate: {
#               call_count, args
#           }
#       }
#   )
    "Case: One commandline":  (
        [   # commandlines,
            'command line 1'
        ],
        [   # popen: [(returncode, [b'stdout'], [b'stderr'])],
            (0, [b'STDOUT'], [b'STDERR'])
        ],
        {   # expected
            'output': b'STDOUT',
            'popen': {
                'call_count': 1,
                'args': [
                    [(['command', 'line', '1'], ), {'stdin': None, 'stdout': _PIPE_, 'stderr': _PIPE_}]
                ]
            },
            'wait': {
                'call_count': 1,
                'args': [
                    [(), {}]
                ]
            }
        }
    ),
    "Case: Two commandlines":  (
        [   # commandlines,
            'cmd 1',
            'cmd 2'
        ],
        [   # popen: [(returncode, b'stdout', b'stderr')],
            (0, [b'STDOUT1'], [b'STDERR1']),
            (0, [b'STDOUT2'], [b'STDERR2'])
        ],
        {   # expected
            'output': b'STDOUT2',
            'popen': {
                'call_count': 2,
                'args': [
                    [(['cmd', '1'], ), {'stdin': None, 'stdout': _PIPE_, 'stderr': _PIPE_}],
                    [(['cmd', '2'], ), {'stdin': [b'STDOUT1'], 'stdout': _PIPE_, 'stderr': _PIPE_}]
                ]
            },
            'wait': {
                'call_count': 2,
                'args': [
                    [(), {}],
                    [(), {}]
                ]
            }
        }
    ),
    "Case: Three commandlines":  (
        [   # commandlines,
            'cmd 1',
            'cmd 2',
            'cmd 3'
        ],
        [   # popen: [(returncode, b'stdout', b'stderr')],
            (0, [b'STDOUT1'], [b'STDERR1']),
            (0, [b'STDOUT2'], [b'STDERR2']),
            (0, [b'STDOUT3'], [b'STDERR3'])
        ],
        {   # expected
            'output': b'STDOUT3',
            'popen': {
                'call_count': 3,
                'args': [
                    [(['cmd', '1'], ), {'stdin': None, 'stdout': _PIPE_, 'stderr': _PIPE_}],
                    [(['cmd', '2'], ), {'stdin': [b'STDOUT1'], 'stdout': _PIPE_, 'stderr': _PIPE_}],
                    [(['cmd', '3'], ), {'stdin': [b'STDOUT2'], 'stdout': _PIPE_, 'stderr': _PIPE_}]
                ]
            },
            'wait': {
                'call_count': 3,
                'args': [
                    [(), {}],
                    [(), {}],
                    [(), {}]
                ]
            }
        }
    ),
}
@pytest.mark.parametrize("commandlines, popen, expected",
    list(_data__run_1.values()), ids=list(_data__run_1.keys()))
def spec__run_1(mocker, commandlines, popen, expected):
    r"""
    [\@spec _run.1] run commandlines with NON-ZERO return_code.
    """
    #
    # Create a mock for subprocess.Popen
    #
    mock_wait = mocker.Mock()

    class dummy_Popen:
        _call_count = 0

        class Stdio:
            def __init__(self, lines):
                self.lines = lines

            def readlines(self):
                return self.lines

        def __init__(self, args, stdin, stdout, stderr):
            self.returncode = popen[dummy_Popen._call_count][0]
            self.stdout = dummy_Popen.Stdio(popen[dummy_Popen._call_count][1])
            self.stderr = dummy_Popen.Stdio(popen[dummy_Popen._call_count][2])
            self.wait = mock_wait
            dummy_Popen._call_count += 1

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    mock_popen = mocker.patch(
        'gdoc.lib.pandocastobject.pandoc.pandoc.subprocess.Popen',
        side_effect=dummy_Popen
    )

    #
    # Execute
    #
    target = Pandoc()
    output = target._run(commandlines)

    #
    # Assert
    #
    assert output == expected['output']

    assert mock_wait.call_count == expected['wait']['call_count']
    assert mock_popen.call_count == expected['popen']['call_count']

    args_popen = mock_popen.call_args_list
    for i in range(mock_popen.call_count):
        if args_popen[i][1]['stdin'] is not None:
            args_popen[i][1]['stdin'] = args_popen[i][1]['stdin'].readlines()

        assert args_popen[i] == expected['popen']['args'][i]

    args_wait = mock_wait.call_args_list
    for i in range(mock_wait.call_count):
        # aseert all args but 1st arg(=self).
        assert args_wait[i] == expected['wait']['args'][i]


_data__run_2 = {
#   id: (
#       commandlines,
#       popen: [(returncode, b'stdout', b'stderr')],
#       expected: {}
#   )
    "Case: One commandline":  (
        [   # commandlines,
            'command line 1'
        ],
        [   # popen: [(returncode, [b'stdout'], [b'stderr'])],
            (1, [b'STDOUT'], [b'STDERR'])
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['command', 'line', '1'],
                'stdout': b'STDOUT',
                'stderr': b'STDERR'
            },
        }
    ),
    "Case: Two commandlines":  (
        [   # commandlines,
            'cmd 1',
            'cmd 2'
        ],
        [   # popen: [(returncode, b'stdout', b'stderr')],
            (0, [b'STDOUT1'], [b'STDERR1']),
            (1, [b'STDOUT2'], [b'STDERR2'])
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['cmd', '2'],
                'stdout': b'STDOUT2',
                'stderr': b'STDERR2'
            },
        }
    ),
    "Case: Three commandlines":  (
        [   # commandlines,
            'cmd 1',
            'cmd 2',
            'cmd 3'
        ],
        [   # popen: [(returncode, b'stdout', b'stderr')],
            (0, [b'STDOUT1'], [b'STDERR1']),
            (1, [b'STDOUT2'], [b'STDERR2']),
            (0, [b'STDOUT3'], [b'STDERR3'])
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['cmd', '2'],
                'stdout': b'STDOUT2',
                'stderr': b'STDERR2'
            },
        }
    ),
}
@pytest.mark.parametrize("commandlines, popen, expected",
    list(_data__run_2.values()), ids=list(_data__run_2.keys()))
def spec__run_2(mocker, commandlines, popen, expected):
    r"""
    [\@spec _run.2] run commandlines with NON-ZERO return_code.
    """
    #
    # Create a mock for subprocess.Popen
    #
    mock_wait = mocker.Mock()

    class dummy_Popen:
        _call_count = 0

        class Stdio:
            def __init__(self, lines):
                self.lines = lines

            def readlines(self):
                return self.lines

        def __init__(self, args, stdin, stdout, stderr):
            self.returncode = popen[dummy_Popen._call_count][0]
            self.stdout = dummy_Popen.Stdio(popen[dummy_Popen._call_count][1])
            self.stderr = dummy_Popen.Stdio(popen[dummy_Popen._call_count][2])
            self.wait = mock_wait
            dummy_Popen._call_count += 1

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    mock_popen = mocker.patch(
        'gdoc.lib.pandocastobject.pandoc.pandoc.subprocess.Popen',
        side_effect=dummy_Popen
    )

    #
    # Execute
    #
    target = Pandoc()
    with pytest.raises(CalledProcessError) as excinfo:
        _ = target._run(commandlines)

    #
    # Assert
    #
    assert excinfo.value.returncode == expected['excinfo']['returncode']
    assert excinfo.value.cmd == expected['excinfo']['cmd']
    assert excinfo.value.stdout == expected['excinfo']['stdout']
    assert excinfo.value.stderr == expected['excinfo']['stderr']

