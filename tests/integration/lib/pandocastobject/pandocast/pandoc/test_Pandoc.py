r"""
The test specification of Pandoc class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/Pandoc]

### THE TARGET

[@import SWDD.SU[Pandoc] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| ------- | ---- | ----------- |
| THIS    | Pandoc       | Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.
| @Method | \_\_init\_\_ | creates a new instance.
| @Method | \_run        | run multiple commands with PIPE and get output.

"""
import pytest
from subprocess import PIPE as _PIPE_
from subprocess import CalledProcessError
from gdoc.lib.pandocastobject.pandoc.pandoc import Pandoc

## @}
## @{ @name _run(self, commandlines, stdin=None)
## [\@test _run] run multiple commands with PIPE and get output.
##

_data__run_1 = {
#   id: (
#       commandlines: [],
#       expected: {}
#   )
    "Case: One commandline":  (
        [   # commandlines,
            '_test_cmd_.sh OUTPUT'
        ],
        {   # expected
            'output':
                b"_test_cmd_ 2.14.2\n"
                b"Commandline opt = OUTPUT\n"
        }
    ),
    "Case: Two commandlines":  (
        [   # commandlines,
            '_test_cmd_.sh ------',
            '_test_cmd_.sh OUTPUT'
        ],
        {   # expected
            'output':
                b"_test_cmd_ 2.14.2\n"
                b"Commandline opt = OUTPUT\n"
        }
    ),
    "Case: Three commandlines":  (
        [   # commandlines,
            '_test_cmd_.sh ------',
            '_test_cmd_.sh ------',
            '_test_cmd_.sh OUTPUT'
        ],
        {   # expected
            'output':
                b"_test_cmd_ 2.14.2\n"
                b"Commandline opt = OUTPUT\n"
        }
    ),
}
@pytest.mark.parametrize("commandlines, expected",
    list(_data__run_1.values()), ids=list(_data__run_1.keys()))
def test__run_1(commandlines, expected):
    r"""
    [\@test _run.1] run commandlines with NON-ZERO return_code.
    """
    here = '/'.join(__file__.split('/')[:-1]) + '/'  # current directory
    cmds = []
    for cmd in commandlines:
        cmds.append(here + cmd)

    target = Pandoc()
    output = target._run(cmds)

    assert output == expected['output']


_data__run_2 = {
#   id: (
#       commandlines: [],
#       expected: {}
#   )
    "Case: One commandline":  (
        [   # commandlines,
            '_test_cmd_.sh'
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['_test_cmd_.sh'],
                'stdout': b'',
                'stderr':
                    b"EXIT(1): NO_OPT\n"
                    b"Try --help for more infomation.\n"
            },
        }
    ),
    "Case: Two commandlines":  (
        [   # commandlines,
            '_test_cmd_.sh --OPTION',
            '_test_cmd_.sh'
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['_test_cmd_.sh'],
                'stdout': b'',
                'stderr':
                    b"EXIT(1): NO_OPT\n"
                    b"Try --help for more infomation.\n"
            },
        }
    ),
    "Case: Three commandlines":  (
        [   # commandlines,
            '_test_cmd_.sh --OPTION',
            '_test_cmd_.sh',
            '_test_cmd_.sh --OPTION'
        ],
        {   # expected
            'excinfo': {
                'returncode': 1,
                'cmd': ['_test_cmd_.sh'],
                'stdout': b'',
                'stderr':
                    b"EXIT(1): NO_OPT\n"
                    b"Try --help for more infomation.\n"
            },
        }
    ),
}
@pytest.mark.parametrize("commandlines, expected",
    list(_data__run_2.values()), ids=list(_data__run_2.keys()))
def test__run_2(commandlines, expected):
    r"""
    [\@test _run.2] run commandlines with NON-ZERO return_code.
    """
    here = '/'.join(__file__.split('/')[:-1]) + '/'  # current directory
    cmds = []
    for cmd in commandlines:
        cmds.append(here + cmd)

    target = Pandoc()
    with pytest.raises(CalledProcessError) as excinfo:
        _ = target._run(cmds)

    assert excinfo.value.returncode == expected['excinfo']['returncode']
    assert excinfo.value.cmd == [here + expected['excinfo']['cmd'][0]] + expected['excinfo']['cmd'][1:]
    assert excinfo.value.stdout == expected['excinfo']['stdout']
    assert excinfo.value.stderr == expected['excinfo']['stderr']
