import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, TypedDict, Union

# =========================
# Base types
# =========================

_Number = Union[int, float]
AnyPacket = Dict[str, Any]
PaletteColor = int
HTMLColor = str
Color = Union[PaletteColor, HTMLColor]
Resources = str
NLUIntent = Dict[str, Any]


class StateName(str, Enum):
    IDLE = "idle"
    ASLEEP = "asleep"
    INTERACTIVE = "interactive"
    PLAYING = "playing"
    RECORDING = "recording"


# =========================
# Base packets
# =========================


class BasePacket(TypedDict):
    type: str


class ServiceRequestPacket(TypedDict, total=False):
    request_id: str


# =========================
# State
# =========================


class StatePacket(TypedDict):
    type: Literal["state"]
    state: StateName


# =========================
# Animation / Info
# =========================


class AnimationItem(TypedDict, total=False):
    left: Color
    center: Color
    right: Color


class Animation(TypedDict):
    tempo: _Number
    colors: List[AnimationItem]


class InfoPacket(ServiceRequestPacket, total=False):
    type: Literal["info"]
    info_id: str
    animation: Animation


# =========================
# Ears
# =========================


class EarsPacket(TypedDict, total=False):
    type: Literal["ears"]
    left: int
    right: int
    event: bool


# =========================
# Command / Message
# =========================

ChoreographyURN = Union[Literal["urn:x-chor:streaming"], str]


class CommandSequenceItem(TypedDict, total=False):
    audio: List[Resources]
    choreography: Union[Resources, ChoreographyURN]


class CommandPacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["command"]
    sequence: List[CommandSequenceItem]
    expiration: datetime.datetime
    cancelable: bool


class MessagePacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["message"]
    body: List[CommandSequenceItem]
    signature: CommandSequenceItem
    expiration: datetime.datetime
    cancelable: bool


# =========================
# Simple commands
# =========================


class CancelPacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["cancel"]


class WakeupPacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["wakeup"]


class SleepPacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["sleep"]


# =========================
# Mode
# =========================

EventTypes = Union[Literal["asr", "button", "ears", "rfid/*"], str]


class ModePacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["mode"]
    mode: Literal["idle", "interactive"]
    events: List[EventTypes]


# =========================
# Test / RFID write
# =========================


class TestPacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["test"]
    test: str


class RfidWritePacket(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["rfid_write"]
    uid: str
    picture: int
    app: int
    tech: str
    timeout: _Number
    data: str


# =========================
# Responses
# =========================


class ResponseBase(TypedDict, ServiceRequestPacket, total=False):
    type: Literal["response"]


class ResponseOKPacket(ResponseBase):
    status: Literal["ok"]


class ResponseCanceledPacket(ResponseBase):
    status: Literal["canceled"]


class ResponseExpiredPacket(ResponseBase):
    status: Literal["expired"]


class ResponseFailurePacket(ResponseBase):
    status: Literal["failure"]


class ResponseErrorPacket(ResponseBase):
    status: Literal["error"]
    class_: str
    message: str


# ---- NFC ----


class ResponseNFCOKPacket(ResponseOKPacket, total=False):
    uid: str


class ResponseNCFErrorPacket(ResponseErrorPacket, total=False):
    uid: str


class ResponseNFCTimeoutPacket(ResponseBase):
    status: Literal["timeout"]
    message: str


# ---- Gestalt ----


class ResponseGestaltPacket(ResponseBase, total=False):
    state: StateName
    connections: int
    hardware: str
    uptime: int


# =========================
# Events
# =========================


class ASREventPacket(TypedDict):
    type: Literal["asr_event"]
    time: float
    nlu: NLUIntent


ButtonEventType = Literal[
    "up",
    "down",
    "click",
    "hold",
    "click_and_hold",
    "double_click",
    "triple_click",
]


class ButtonEventPacket(TypedDict):
    type: Literal["button_event"]
    time: float
    event: ButtonEventType


class EarEventPacket(TypedDict):
    type: Literal["ear_event"]
    time: float
    ear: Literal["left", "right"]


class EarsEventPacket(TypedDict):
    type: Literal["ears_event"]
    time: float
    left: int
    right: int


class RfidEventPacket(TypedDict, total=False):
    type: Literal["rfid_event"]
    time: float
    tech: str
    uid: str
    event: Literal["removed", "detected"]
    support: Literal["formatted", "foreign-data", "locked", "empty", "unknown"]
    locked: bool
    picture: str
    tag_info: dict
    app: str
    data: str


# =========================
# Unions
# =========================

ResponsePacket = Union[
    ResponseOKPacket,
    ResponseCanceledPacket,
    ResponseExpiredPacket,
    ResponseFailurePacket,
    ResponseErrorPacket,
    ResponseGestaltPacket,
    ResponseNFCOKPacket,
    ResponseNCFErrorPacket,
    ResponseNFCTimeoutPacket,
]

EventPacket = Union[
    ASREventPacket,
    ButtonEventPacket,
    EarEventPacket,
    EarsEventPacket,
    RfidEventPacket,
]

ServicePacket = Union[
    InfoPacket,
    EarsPacket,
    CommandPacket,
    MessagePacket,
    CancelPacket,
    WakeupPacket,
    SleepPacket,
    ModePacket,
    RfidWritePacket,
    TestPacket,
]

NabdPacket = Union[StatePacket, ResponsePacket, EventPacket]
