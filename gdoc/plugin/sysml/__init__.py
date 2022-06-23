from . import block, requirement

exports = {
    "Table": {
        "requirement": {"constructor": requirement.Requirement},
        "reqt": {"constructor": requirement.Requirement},
        "block": {"constructor": block.Block},
        "blk": {"constructor": block.Block},
    }
}
