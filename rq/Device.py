from dataclasses import dataclass
from typing import List


# struct for device

@dataclass
class Ethernet:
    port: int
    speed: int

    def __str__(self):
        return f"port: {self.port} ;  speed: {self.speed} "


@dataclass
class Wireless:
    rssi0: int
    rssi1: int
    rssi2: int
    mcs: int
    rate: int
    idle: int

    def __str__(self):
        return f"rssi0: {self.rssi0} ; rssi1: {self.rssi1} ; rssi2: {self.rssi2} ; mcs: {self.mcs} ; rate: {self.rate} ; idle: {self.idle} "


@dataclass
class Ipv6Addr:
    ip6address: str

    def __str__(self):
        return f"ip6address: {self.ip6address} "


@dataclass
class Device:
    id: int
    hostname: str
    macaddress: str
    ipaddress: str
    type: str
    link: str
    lease: int
    active: bool
    lastseen: str  # ISO TIME STRING

    ethernet: dict
    wireless: dict
    ip6address: list

    def get_ethernet(self) -> Ethernet:
        return Ethernet(**self.ethernet)

    def get_wireless(self) -> Wireless:
        return Wireless(**self.wireless)

    def get_ipv6(self) -> List[Ipv6Addr]:
        for ipaddr in self.ip6address:
            yield Ipv6Addr(ipaddr.get("ipaddress", ""))

    def __str__(self):
        return f"{self.hostname} {self.mac} {self.ip} {self.active} "
