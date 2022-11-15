import json
from typing import Any

import pytest

from gdoc.lib.pandocastobject.pandoc import Pandoc
from gdoc.lib.pandocastobject.pandocast import PandocAst, PandocElement


@pytest.fixture
def test_data_from_pandoc():
    def get_test_data_from_pandoc(
        filepath: str, formattype: str, html: bool
    ) -> tuple[PandocElement | list[PandocElement], Any]:

        # Read file and get pandocAST
        pandoc_json = Pandoc().get_json(filepath, formattype, html)
        pandoc_ast = PandocAst(pandoc_json)
        index_json = pandoc_ast.get_child_items()[-1].get_content()
        index: dict = json.loads(index_json)

        # Get test parameter
        test_param: Any
        param_json = pandoc_ast.get_child_items()[index["test_param"]].get_content()
        test_param = json.loads(param_json)

        # Get test block
        test_block: PandocElement | list[PandocElement]
        index_test_block = index["test_block"]

        if index_test_block is None:
            test_block = pandoc_ast

        elif type(index_test_block) is int:
            test_block = pandoc_ast.get_child_items()[index_test_block]

        else:  # list
            test_block = []
            for i in index_test_block:
                test_block.append(pandoc_ast.get_child_items()[i])

        return test_block, test_param

    return get_test_data_from_pandoc
