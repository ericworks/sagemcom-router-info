from dataclasses import dataclass


@dataclass
class Cellular:
    duration: str  # in seconds
    data: dict  # number of Bytes

    def get_session_duration_in_seconds(self) -> int:
        return int(self.duration)

    def get_data_in_byte(self) -> int:
        return int(self.data.get("received", ""))

    def get_data_out_byte(self) -> int:
        return int(self.data.get("sent", ""))