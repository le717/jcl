from dataclasses import dataclass
from enum import Enum
from os import fspath
from pathlib import Path
from re import match
from typing import Any, List, Optional, Union

__all__ = ["Config"]


class Delimiters(Enum):
    Comment = "!|#"
    Command = "\n"


@dataclass
class ParserReply:
    status: bool
    msg: str
    data: Optional[Any] = None


class Config:
    def __init__(self, config_path: str):
        self.config_path: Union[Path, str] = config_path
        self.config_data: Optional[List[str]] = None

    def __make_error(self, msg: str) -> ParserReply:
        return self.__make_reply(False, msg)

    def __make_reply(
        self, status: bool, msg: str, data: Optional[Any] = None
    ) -> ParserReply:
        return ParserReply(status, msg, data)

    def __strip_blanks(self, text: list) -> list:
        return [line.strip() for line in text if line]

    def __strip_comments(self, text: list) -> list:
        return [line for line in text if match(Delimiters.Comment.value, line) is None]

    def load(self) -> ParserReply:
        # Try to find the given config file
        self.config_path = Path(self.config_path).resolve()

        # Yeah, it doesn't exist or isn't an actual file
        if not self.config_path.exists() and not self.config_path.is_file():
            return self.__make_error(
                f"The Juniper config file could not be found at {fspath(self.config_path)}"  # noqa
            )

        # Well now, it actually exists! The contractor actually _did_ something!
        return self.__make_reply(
            True,
            f"Successfully found Juniper config at {fspath(self.config_path)}",  # noqa
        )

    def parse(self):
        # Get the file content
        file_contents = self.config_path.read_text().split(Delimiters.Command.value)

        # Clean up and parse out the commands
        file_contents = self.__strip_blanks(file_contents)
        file_contents = self.__strip_comments(file_contents)
        self.config_data = file_contents
        return ParserReply(True, "Juniper config sucessfully loaded")
