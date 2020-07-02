from time import sleep
from typing import Callable, Union

import serial

__all__ = ["Connection"]


class Connection:
    """Connect to a device over a serial line."""

    def __init__(self, line: str) -> None:
        self.com_port: str = f"COM{line}"
        self.connection: serial.Serial = serial.Serial(self.com_port, timeout=5)  # noqa

    def disconnect(self) -> bool:
        """Disconnect from the device."""
        self.connection.close()
        return not self.connection.is_open

    def repeat(self, func: Callable, *, times: int) -> "Connection":
        """Repeat a class method a set number of times."""
        for _ in range(times):
            func()
        return self

    def send(self, command: str, wait: Union[int, float] = 0) -> "Connection":
        """Send a command to the device."""
        self.connection.write(command.encode("utf-8"))
        sleep(wait)
        return self

    def enter_key(self, *, wait: Union[int, float] = 0) -> "Connection":
        """Send an enter key press."""
        self.send("\r")
        sleep(wait)
        return self

    def exit(self) -> "Connection":
        """Send an exit command."""
        self.send("exit").enter_key(wait=1.25)
        return self
