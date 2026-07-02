# Expose controller at package level
from .instrument import InstrumentController, example_workflow

__all__ = ["InstrumentController", "example_workflow"]
