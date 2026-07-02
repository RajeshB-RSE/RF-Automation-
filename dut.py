"""DUT controller stubs.

This module contains a DUTController class with scaffolded methods for
NanoKDP / UART communication. Replace stubs with real implementations
using pyserial, vendor SDKs, or other interfaces as needed.
"""
from dataclasses import dataclass
from typing import Optional, List
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class DUTController:
    """Controller for Device Under Test (DUT).

    This is a scaffold. Implement real communication (NanoKDP, serial)
    according to your DUT APIs.
    """
    address: Optional[str] = None
    connected: bool = False

    def detect_device(self) -> Optional[str]:
        """Attempt to detect the DUT automatically.

        Return a detected address or None.
        """
        # TODO: implement auto-detection (list serial ports, KOBA discovery, etc.)
        logger.debug("Detecting DUT... (stub)")
        return None

    def connect_uart(self, port: str, baudrate: int = 115200, timeout: float = 1.0) -> bool:
        """Connect to DUT over UART/serial.

        Replace this stub with pyserial-based implementation.
        """
        logger.info("Connecting to DUT at %s (baud=%s)", port, baudrate)
        # Simulate connection
        time.sleep(0.1)
        self.address = port
        self.connected = True
        return self.connected

    def connect_nanokdp(self, address: str) -> bool:
        """Connect to DUT via NanoKDP (stub)."""
        logger.info("Connecting to DUT via NanoKDP at %s", address)
        time.sleep(0.1)
        self.address = address
        self.connected = True
        return True

    def send_command(self, cmd: str, wait: float = 0.1) -> str:
        """Send a single command to the DUT and return the response (stub)."""
        if not self.connected:
            raise RuntimeError("DUT not connected")
        logger.debug("Sending command to DUT: %s", cmd)
        time.sleep(wait)
        # Return a fake response
        return "OK"

    def run_script_file(self, path: str) -> List[str]:
        """Execute a script file containing DUT commands (one per line).

        Returns list of responses.
        """
        if not self.connected:
            raise RuntimeError("DUT not connected")
        responses = []
        logger.info("Running DUT script: %s", path)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # handle WAIT n
                    if line.upper().startswith("WAIT"):
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                ms = int(parts[1])
                                logger.debug("WAIT %s ms", ms)
                                time.sleep(ms / 1000.0)
                                responses.append("WAIT")
                                continue
                            except ValueError:
                                pass
                    resp = self.send_command(line)
                    responses.append(resp)
        except FileNotFoundError:
            logger.error("Script file not found: %s", path)
            raise
        return responses

    def reset(self) -> bool:
        """Reset the DUT (stub)."""
        if not self.connected:
            raise RuntimeError("DUT not connected")
        logger.info("Resetting DUT (stub)")
        time.sleep(0.2)
        return True

    def get_battery_status(self) -> dict:
        """Return a stubbed battery status.

        Replace with real monitoring commands.
        """
        if not self.connected:
            raise RuntimeError("DUT not connected")
        return {"level_percent": 95, "charging": False}

    def get_baseband_status(self) -> dict:
        """Return a stubbed baseband status (e.g., firmware, state)."""
        if not self.connected:
            raise RuntimeError("DUT not connected")
        return {"firmware": "v1.0.0", "state": "idle"}
