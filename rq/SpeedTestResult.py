from dataclasses import dataclass


@dataclass
class SpeedTestResult:
    download: float
    upload: float
    ping: float
    timestamp: str

    bytes_sent: int
    bytes_received: int

    server: dict
    client: dict

    client_ip = lambda s: s.client["ip"]
    client_isp = lambda s: s.client["isp"]

    server_name = lambda s: s.sponsor  # sponsor
    server_city = lambda s: s.name  # name

    def __str__(self):
        return f"Download: {self.download} bps\nUpload: {self.upload} bps\nPing: {self.ping} ms\nTimestamp: {self.timestamp}\nBytes Sent: {self.bytes_sent}\nBytes Received: {self.bytes_received}\nServer: {self.server}\nClient: {self.client}"
