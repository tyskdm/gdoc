r"""
The test specification of Pandoc class.

### REFERENCES

[@import SWDD from=gdoc/docs/ArchitecturalDesign/PandocAstObject/Pandoc]

### THE TARGET

[@import SWDD.SU[Pandoc] as=THIS]

### ADDITIONAL STRUCTURE

| @Class& | Name | Description |
| --version- | ---- | --version----- |
| THIS    | Pandoc       | Execute external pandoc command as a subprocess to parse a source md file to generate PandocAST json object.
| @Method | \_\_init\_\_ | creates a new instance.
| @Method | \_run        | run multiple commands with PIPE and get output.

"""
import json

import pytest

from gdoc.lib.pandocastobject.pandoc.pandoc import Pandoc


class Test__run:
    """
    [@test _run] run multiple commands with PIPE and return results.
    def _run(
        self, commandlines: list[list[str]], stdin=None
    ) -> tuple[list[int], str, list[str]]:
    """

    case_1 = {
        "Case: One commandline": (
            # stimulus
            [
                "_test_cmd_.sh OPTION",
            ],
            # expected
            {
                "output": (
                    [0],
                    "Exit(0): WITH_OPT\n" "OPT = OPTION\n",
                    [""],
                )
            },
        ),
        "Case: Two commandlines": (
            # stimulus
            [
                "_test_cmd_.sh OPTION",
                "_test_cmd_.sh OPTION",
            ],
            # expected
            {
                "output": (
                    [0, 0],
                    "Exit(0): WITH_OPT\n" "OPT = OPTION\n",
                    ["", ""],
                )
            },
        ),
        "Case: Three commandlines": (
            # stimulus
            [
                "_test_cmd_.sh OPTION",
                "_test_cmd_.sh OPTION",
                "_test_cmd_.sh OPTION",
            ],
            # expected
            {
                "output": (
                    [0, 0, 0],
                    "Exit(0): WITH_OPT\n" "OPT = OPTION\n",
                    ["", "", ""],
                )
            },
        ),
        #
        # Error cases
        #
        "Error: One commandline": (
            # stimulus
            [
                "_test_cmd_.sh",
            ],
            # expected
            {
                "output": (
                    [1],
                    "",
                    ["EXIT(1): NO_OPT\n"],
                )
            },
        ),
        "Error: Two commandlines": (
            # stimulus
            [
                "_test_cmd_.sh OPTION",
                "_test_cmd_.sh",
            ],
            # expected
            {
                "output": (
                    [0, 1],
                    "",
                    ["", "EXIT(1): NO_OPT\n"],
                )
            },
        ),
        "Error: Three commandlines": (
            # stimulus
            [
                "_test_cmd_.sh OPTION",
                "_test_cmd_.sh",
                "_test_cmd_.sh OPTION",
            ],
            # expected
            {
                "output": (
                    [0, 1, 0],
                    "Exit(0): WITH_OPT\n" "OPT = OPTION\n",
                    ["", "EXIT(1): NO_OPT\n", ""],
                )
            },
        ),
    }

    @pytest.mark.parametrize(
        "stimulus, expected",
        list(case_1.values()),
        ids=list(case_1.keys()),
    )
    def test_1(self, stimulus, expected):
        here = __file__.rsplit("/", 1)[0] + "/"  # current directory

        # WHEN
        commandlines = [(here + cmd).split() for cmd in stimulus]
        output = Pandoc()._run(commandlines)

        # THEN
        assert output == expected["output"]


class Test_get_version:
    """
    [@test get_version] returns versions of pandoc and pandoc-types.
    """

    case_1 = {
        "Normal Case: Actual output from pnadoc": (
            # precondition
            "_test_cmd_.sh",
            # expected
            {
                "pandoc": [2, 14, 2],
                "pandoc-types": [1, 22, 2, 1],
            },
        ),
    }

    @pytest.mark.parametrize(
        "precondition, expected",
        list(case_1.values()),
        ids=list(case_1.keys()),
    )
    def test_1(self, mocker, precondition, expected):
        here = __file__.rsplit("/", 1)[0] + "/"  # current directory

        target = Pandoc(here + precondition)
        output = target.get_version()

        assert output == expected


class Test_get_json:
    """
    [@test get_version] returns versions of pandoc and pandoc-types.
    """

    case_1 = {
        "Case: No opt": (
            # precondition
            "test_1.md",
            # stimulus
            None,
            # expected
            "test_1_md(NO_OPT).json",
        ),
        "Case: html = False": (
            # precondition
            "test_1.md",
            # stimulus
            ["gfm-sourcepos", False],
            # expected
            "test_1_md(html_false).json",
        ),
        "Case: html = True": (
            # precondition
            "test_1.md",
            # stimulus
            ["gfm-sourcepos", True],
            # expected
            "test_1_md(html_true).json",
        ),
        "Case: gfm / html = True": (
            # precondition
            "test_1.md",
            # stimulus
            ["gfm", True],
            # expected
            "test_1_md(gfm_html_true).json",
        ),
    }

    @pytest.mark.parametrize(
        "precondition, stimulus, expected",
        list(case_1.values()),
        ids=list(case_1.keys()),
    )
    def test_1(self, monkeypatch, precondition, stimulus, expected):
        r"""
        [\@test get_json.1] run pandoc and get json object.
        """
        datadir = __file__.split(".", 1)[0]  # data directory
        monkeypatch.chdir(datadir)

        # GIVEN
        filepath = precondition

        # WHEN
        if stimulus is not None:
            output = Pandoc().get_json(filepath, stimulus[0], stimulus[1])
        else:
            output = Pandoc().get_json(filepath)

        # THEN
        with open(expected, "r", encoding="UTF-8") as f:
            expected_json = json.load(f)

        del output["pandoc-api-version"]
        del expected_json["pandoc-api-version"]

        assert output == expected_json
