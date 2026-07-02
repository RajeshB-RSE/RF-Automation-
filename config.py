"""Configuration utilities for RF Automation.

This module provides a simple configuration dataclass and a JSON loader.
You can extend this to support YAML or TOML if desired.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class InstrumentConfig:
    name: str
    address: Optional[str] = None
    params: Dict[str, Any] = None


def load_config_from_json(path: str) -> Dict[str, Any]:
    """Load a JSON config file and return as a dict.

    Example structure:
    {
      "dut": {"name": "DUT", "address": "COM3", "params": {}},
      "cmw500": {"name": "CMW500", "address": "TCPIP::192.168.0.10::INSTR"},
      "fsw": {"name": "FSW", "address": "TCPIP::192.168.0.11::INSTR"}
    }
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
        return cfg
    except Exception as e:
        logger.error("Failed to load config from %s: %s", path, e)
        raise
