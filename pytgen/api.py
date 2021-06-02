from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class RangeValues:
    start: int = 0
    step: int = 1
    end: int = 1


@dataclass
class RandomValues:
    min: int = 0
    max: int = 1
    count: int = 1


@dataclass
class FieldPattern:
    bit_offset: int = 12
    bit_length: int = 8
    values: Union[List[int], RangeValues, RandomValues] = field(default_factory=list)


@dataclass
class ChecksumField:
    start_bit: int
    end_bit: int
    position_bit: int
    bit_length: int


@dataclass
class Flow:
    name: str
    tx: str
    rx: Union[str, None] = None
    frame_bytes: bytes = b"\x00" * 60
    frame_count: int = 1
    frame_size: Union[int, List[int], RangeValues, RandomValues] = 64
    field_patterns: List[FieldPattern] = field(default_factory=list)
    checksum_fields: List[ChecksumField] = field(default_factory=list)
    start_delay_ns: int = 0


@dataclass
class Port:
    name: str
    location: str
    capture: bool = False


@dataclass
class Config:
    name: str
    ports: List[Port] = field(default_factory=list)
    flows: List[Flow] = field(default_factory=list)


@dataclass
class PortMetrics:
    name: str
    tx_frames: int = 0
    rx_frames: int = 0
    tx_fps: int = 0
    rx_fps: int = 0


@dataclass
class FlowMetrics:
    name: str
    tx_name: str
    rx_name: Union[str, None] = None
    tx_frames: int = 0
    rx_frames: int = 0
    tx_fps: int = 0
    rx_fps: int = 0


@dataclass
class Capture:
    timstamp_ns: float = 0
    frame_bytes: bytes = b""


class Session:
    def __init__(self) -> None:
        self.config: Union[Config, None] = None

    def set_config(self, config: Config) -> None:
        raise NotImplementedError

    def start_flows(self, flow_names: List[str] = []) -> None:
        raise NotImplementedError

    def stop_flows(self, flow_names: List[str] = []) -> None:
        raise NotImplementedError

    def get_port_metrics(self, port_names: List[str] = []) -> List[PortMetrics]:
        raise NotImplementedError

    def get_flow_metrics(self, flow_names: List[str] = []) -> List[FlowMetrics]:
        raise NotImplementedError

    def get_captures(self, port_name: str) -> List[Capture]:
        raise NotImplementedError
