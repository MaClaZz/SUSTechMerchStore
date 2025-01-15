from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LogMessage(_message.Message):
    __slots__ = ("message", "timestamp")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message: str
    timestamp: str
    def __init__(self, message: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class LogResponse(_message.Message):
    __slots__ = ("confirmation",)
    CONFIRMATION_FIELD_NUMBER: _ClassVar[int]
    confirmation: str
    def __init__(self, confirmation: _Optional[str] = ...) -> None: ...
