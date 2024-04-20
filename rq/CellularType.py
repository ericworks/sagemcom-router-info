from enum import Enum


class CellularType(Enum):
    t_4G = "4G"
    t_5G_NSA = "5GNSA"
    DISCONNECT = "NA"

    def __str__(self):
        return self.name
