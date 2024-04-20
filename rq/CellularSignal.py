from dataclasses import dataclass


@dataclass
class CellularSignal:
    rssi: int
    rsrp: int
    rsrq: int
    txpower: float
    tac: str
    bandinfo: str  #earfcn
    mcc: str
    mnc: str
    status: str
    enable: bool