from typing import Tuple, TypeVar

import bittensor as bt

from mining import core_miner
from mining.operations import abstract_operation
from models import base_models, protocols
from operation_logic import scribble_logic

operation_name = "ScribbleOperation"

T = TypeVar("T", bound=bt.Synapse)


class ScribbleOperation(abstract_operation.Operation):
    @staticmethod
    async def forward(synapse: protocols.Scribble) -> protocols.Scribble:
        output = await scribble_logic.scribble_logic(base_models.ScribbleIncoming(**synapse.dict()))

        synapse.init_image = None

        output_dict = output.dict()
        for field in output_dict:
            setattr(synapse, field, output_dict[field])

        return synapse

    @staticmethod
    def blacklist(synapse: protocols.Scribble) -> Tuple[bool, str]:
        return core_miner.base_blacklist(synapse)

    @staticmethod
    def priority(synapse: protocols.Scribble) -> float:
        return core_miner.base_priority(synapse)
