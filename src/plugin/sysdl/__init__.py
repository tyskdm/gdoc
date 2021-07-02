from . import requirement
from . import block

exports = {
    "Table": {
        "requirement": {
            "constructor": requirement.Requirement
        },
        "reqt": {
            "constructor": requirement.Requirement
        },
        "block": {
            "constructor": block.Block
        },
        "blk": {
            "constructor": block.Block
        }
    }
}

