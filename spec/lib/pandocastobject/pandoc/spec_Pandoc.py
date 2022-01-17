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
    [\@spec _run.1] run commandlines with NO-ERROR.
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


## @}
## @{ @name get_version(self)
## [\@spec get_version] returns versions of pandoc and pandoc-types.
##

_data_get_version_1 = {
#   id: (
#       stdout: b'output string'
#       expected: {
#           output: {},
#           _run: {}
#       ]
#   )
    "Normal Case: Actual output from pnadoc":  (
        b'pandoc 2.14.2\n' +
        b'Compiled with pandoc-types 1.22, texmath 0.12.3.1, skylighting 0.11,\n' +
        b'citeproc 0.5, ipynb 0.1.0.1\n',
        # expected
        {
            'output': {
                'pandoc': [2, 14, 2],
                'pandoc-types': [1, 22]
            },
            '_version_str':
                'pandoc 2.14.2\n' +
                'Compiled with pandoc-types 1.22, texmath 0.12.3.1, skylighting 0.11,\n' +
                'citeproc 0.5, ipynb 0.1.0.1\n',
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Normal Case: Output in different format(1)":  (
        b'pandoc 2.14.2, << FLLOWING SOME STRING\n' +
        b'PLACED THE END OF LINE >> pandoc-types 1.22\n',
        # expected
        {
            'output': {
                'pandoc': [2, 14, 2],
                'pandoc-types': [1, 22]
            },
            '_version_str':
                'pandoc 2.14.2, << FLLOWING SOME STRING\n' +
                'PLACED THE END OF LINE >> pandoc-types 1.22\n',
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Normal Case: Output in different format(2)":  (
        b'pandoc-types 1.22\n' +
        b'pandoc 2.14.2\n',
        # expected
        {
            'output': {
                'pandoc': [2, 14, 2],
                'pandoc-types': [1, 22]
            },
            '_version_str':
                'pandoc-types 1.22\n' +
                'pandoc 2.14.2\n',
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Normal Case: Version strings are not only decimal char":  (
        b'pandoc 2.14b.2\n' +
        b'pandoc-types 1.22a\n',
        # expected
        {
            'output': {
                'pandoc': [2, '14b', 2],
                'pandoc-types': [1, '22a']
            },
            '_version_str':
                'pandoc 2.14b.2\n' +
                'pandoc-types 1.22a\n',
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Normal Case: Skip if version string does not start with decimal char":  (
        b'pandoc NOT.VERSION.STRING\n' +
        b'pandoc 2.14.2\n' +
        b'pandoc-types 1.22\n',
        # expected
        {
            'output': {
                'pandoc': [2, 14, 2],
                'pandoc-types': [1, 22]
            },
            '_version_str':
                'pandoc NOT.VERSION.STRING\n' +
                'pandoc 2.14.2\n' +
                'pandoc-types 1.22\n',
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Error Case: One of version string is missing":  (
        b'pandoc 2.14.2\n' +
        b'VER-STR IS MISSING >> pandoc-types\n',
        # expected
        {
            'output': None,
            '_version_str': None,
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    ),
    "Error Case: One of version string does not start with decimal char":  (
        b'pandoc NOT.VERSION.STRING\n' +
        b'pandoc-types 1.22a\n',
        # expected
        {
            'output': None,
            '_version_str': None,
            '_run': {
                'call_count': 1,
                'args': [(['pandoc --version'],), {}]
            }
        }
    )
}
@pytest.mark.parametrize("stdout, expected",
    list(_data_get_version_1.values()), ids=list(_data_get_version_1.keys()))
def spec_get_version_1(mocker, stdout, expected):
    r"""
    [\@spec get_version.1] returns generated version info for the first time.
    """
    mock__run = mocker.Mock(return_value = stdout)

    target = Pandoc()
    target._run = mock__run
    output = target.get_version()

    assert output == expected['output']
    assert target._version_str == expected['_version_str']

    args__run = mock__run.call_args_list
    assert mock__run.call_count == expected['_run']['call_count']
    assert args__run[0] == expected['_run']['args']


def spec_get_version_2(mocker):
    r"""
    [\@spec get_version.2] returns stored version info for the second time.
    """
    _VERSION_ = {
        'pandoc': [0, 0, 0],
        'pandoc-types': [0, 0]
    },
    mock__run = mocker.Mock()

    target = Pandoc()
    target._run = mock__run
    target._version = _VERSION_
    output = target.get_version()

    assert mock__run.call_count == 0
    assert output == _VERSION_


## @}
## @{ @name get_json(self, filepath, fromType=None, html=False)
## [\@spec get_json] returns pandoc ast json object.
##

_data_get_json_1 = {
#   id: (
#       args: [filepath, filetype, html]
#       expected: {
#           call_count: int
#           commandlines: [commandline]
#       }
#   )
    "Case: .md with NO other arguments": (
        ['TEST.md'],
        [
            'pandoc TEST.md -f gfm+sourcepos -t html',
            'pandoc -f html -t json'
        ]
    ),
    "Case: .md with default arguments": (
        ['TEST.md', None, None],
        [
            'pandoc TEST.md -f gfm+sourcepos -t html',
            'pandoc -f html -t json'
        ]
    ),
    "Case: .MD with default arguments": (
        ['TEST.MD', None, None],
        [
            'pandoc TEST.MD -f gfm+sourcepos -t html',
            'pandoc -f html -t json'
        ]
    ),
    "Case: .rst with default arguments": (
        ['TEST.rst', None, None],
        ['pandoc TEST.rst -t json']
    ),
    "Case: Long path with default arguments": (
        ['/path/to/TEST.rst', None, None],
        ['pandoc /path/to/TEST.rst -t json']
    ),
    "Case: No ext with default arguments": (
        ['/path/to/TEST', None, None],
        ['pandoc /path/to/TEST -t json']
    ),
    "Case: Filename includeing double '.' with default arguments": (
        ['/path/to/TE.ST.rst', None, None],
        ['pandoc /path/to/TE.ST.rst -t json']
    ),
    "Case: Filepath endswith('/') with default arguments": (
        ['/path/to/documents/', None, None],
        ['pandoc /path/to/documents/ -t json']
    ),
    "Case: .md with specified filetype 'markdown'": (
        ['TEST.md', 'markdown', None],
        ['pandoc TEST.md -f markdown -t json']
    ),
    "Case: .rst with specified filetype 'rst'": (
        ['TEST.rst', 'rst', None],
        ['pandoc TEST.rst -f rst -t json']
    ),
    "Case: .md with html=False": (
        ['TEST.md', None, False],
        ['pandoc TEST.md -t json']
    ),
    "Case: .md with html=True": (
        ['TEST.md', None, True],
        [
            'pandoc TEST.md -t html',
            'pandoc -f html -t json'
        ]
    ),
    "Case: .md with arguments, filetype='markdown' and html=True": (
        ['TEST.md', 'markdown', True],
        [
            'pandoc TEST.md -f markdown -t html',
            'pandoc -f html -t json'
        ]
    ),
    "Case: .md with arguments, filetype='markdown' and html=False": (
        ['TEST.md', 'markdown', False],
        ['pandoc TEST.md -f markdown -t json']
    ),
    "Case: filetype='commonmark' should be added '+sourcepos'": (
        ['TEST.md', 'commonmark', False],
        ['pandoc TEST.md -f commonmark+sourcepos -t json']
    ),
    "Case: filetype='gfm' should be added '+sourcepos'": (
        ['TEST.md', 'gfm', False],
        ['pandoc TEST.md -f gfm+sourcepos -t json']
    ),
}
@pytest.mark.parametrize("args, expected",
    list(_data_get_json_1.values()), ids=list(_data_get_json_1.keys()))
def spec_get_json_1(mocker, args, expected):
    r"""
    [\@spec get_json.1] Generates and returns an object according to its arguments.
    """
    mock__run = mocker.Mock(return_value = b'{"TEST_KEY":"TEST_VALUE"}')

    target = Pandoc()
    target._run = mock__run

    if len(args) > 2:
        output = target.get_json(args[0], args[1], args[2])
    else:
        output = target.get_json(args[0])

    args__run = mock__run.call_args_list
    assert mock__run.call_count == 1
    assert args__run[0] == ((expected,), {})
    assert output == {'TEST_KEY':'TEST_VALUE'}


