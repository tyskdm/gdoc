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
import json
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
    "Case: One commandline": (
        ["_test_cmd_.sh OUTPUT"],  # commandlines,
        {"output": b"_test_cmd_ 2.14.2\n" b"Commandline opt = OUTPUT\n"},  # expected
    ),
    "Case: Two commandlines": (
        ["_test_cmd_.sh ------", "_test_cmd_.sh OUTPUT"],  # commandlines,
        {"output": b"_test_cmd_ 2.14.2\n" b"Commandline opt = OUTPUT\n"},  # expected
    ),
    "Case: Three commandlines": (
        ["_test_cmd_.sh ------", "_test_cmd_.sh ------", "_test_cmd_.sh OUTPUT"],  # commandlines,
        {"output": b"_test_cmd_ 2.14.2\n" b"Commandline opt = OUTPUT\n"},  # expected
    ),
}


@pytest.mark.parametrize(
    "commandlines, expected", list(_data__run_1.values()), ids=list(_data__run_1.keys())
)
def test__run_1(commandlines, expected):
    r"""
    [\@test _run.1] run commandlines with NON-ZERO return_code.
    """
    here = "/".join(__file__.split("/")[:-1]) + "/"  # current directory
    cmds = []
    for cmd in commandlines:
        cmds.append(here + cmd)

    target = Pandoc()
    output = target._run(cmds)

    assert output == expected["output"]


_data__run_2 = {
    #   id: (
    #       commandlines: [],
    #       expected: {}
    #   )
    "Case: One commandline": (
        ["_test_cmd_.sh"],  # commandlines,
        {  # expected
            "excinfo": {
                "returncode": 1,
                "cmd": ["_test_cmd_.sh"],
                "stdout": b"",
                "stderr": b"EXIT(1): NO_OPT\n" b"Try --help for more infomation.\n",
            },
        },
    ),
    "Case: Two commandlines": (
        ["_test_cmd_.sh --OPTION", "_test_cmd_.sh"],  # commandlines,
        {  # expected
            "excinfo": {
                "returncode": 1,
                "cmd": ["_test_cmd_.sh"],
                "stdout": b"",
                "stderr": b"EXIT(1): NO_OPT\n" b"Try --help for more infomation.\n",
            },
        },
    ),
    "Case: Three commandlines": (
        ["_test_cmd_.sh --OPTION", "_test_cmd_.sh", "_test_cmd_.sh --OPTION"],  # commandlines,
        {  # expected
            "excinfo": {
                "returncode": 1,
                "cmd": ["_test_cmd_.sh"],
                "stdout": b"",
                "stderr": b"EXIT(1): NO_OPT\n" b"Try --help for more infomation.\n",
            },
        },
    ),
}


@pytest.mark.parametrize(
    "commandlines, expected", list(_data__run_2.values()), ids=list(_data__run_2.keys())
)
def test__run_2(commandlines, expected):
    r"""
    [\@test _run.2] run commandlines with NON-ZERO return_code.
    """
    here = "/".join(__file__.split("/")[:-1]) + "/"  # current directory
    cmds = []
    for cmd in commandlines:
        cmds.append(here + cmd)

    target = Pandoc()
    with pytest.raises(CalledProcessError) as excinfo:
        _ = target._run(cmds)

    assert excinfo.value.returncode == expected["excinfo"]["returncode"]
    assert (
        excinfo.value.cmd == [here + expected["excinfo"]["cmd"][0]] + expected["excinfo"]["cmd"][1:]
    )
    assert excinfo.value.stdout == expected["excinfo"]["stdout"]
    assert excinfo.value.stderr == expected["excinfo"]["stderr"]


## @}
## @{ @name get_version(self)
## [\@test get_version] returns versions of pandoc and pandoc-types.
##

_data_get_version_1 = {
    #   id: (
    #       stdout: b'output string'
    #       expected: [
    #           pandoc_version: [int],
    #           pandoc_types: [int]
    #       ]
    #   )
    "Normal Case: Actual output from pnadoc": (
        b"pandoc 2.14.2\n" + b"Compiled with pandoc-types 1.22,",
        # expected
        {
            "output": {"pandoc": [2, 14, 2], "pandoc-types": [1, 22]},
            "_run": {"call_count": 1, "args": [(["pandoc --version"],), {}]},
        },
    ),
}


@pytest.mark.parametrize(
    "stdout, expected", list(_data_get_version_1.values()), ids=list(_data_get_version_1.keys())
)
def test_get_version_1(mocker, stdout, expected):
    r"""
    [\@test get_version.1] run commandlines with NON-ZERO return_code.
    """
    target = Pandoc()
    output = target.get_version()

    assert output == expected["output"]
    assert target._version_str.startswith(stdout.decode())


## @}
## @{ @name get_version(self)
## [\@test get_version] returns versions of pandoc and pandoc-types.
##

_data_get_json_1 = {
    #   id: (
    #       filename: str,
    #       args: (filetype, html)
    #       jsonfile: jsonfilename
    #   )
    "Case: No opt": ("test_1.md", None, "test_1_md(NO_OPT).json"),
    "Case: html = False": ("test_1.md", [None, False], "test_1_md(html_false).json"),
    "Case: html = True": ("test_1.md", [None, True], "test_1_md(html_true).json"),
}


@pytest.mark.parametrize(
    "filename, args, jsonfile", list(_data_get_json_1.values()), ids=list(_data_get_json_1.keys())
)
def test_get_json_1(monkeypatch, filename, args, jsonfile):
    r"""
    [\@test get_json.1] run pandoc and get json object.
    """
    datadir = ".".join(__file__.split(".")[:-1])  # data directory
    monkeypatch.chdir(datadir)

    target = Pandoc()

    if args is not None:
        output = target.get_json(filename, args[0], args[1])
    else:
        output = target.get_json(filename)

    with open(jsonfile, "r", encoding="UTF-8") as f:
        expected = json.load(f)

    assert output == expected
