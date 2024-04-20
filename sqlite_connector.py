from __future__ import annotations

import json
import sqlite3

from rq.CellularSignal import CellularSignal
from rq.Device import Device
from rq.SpeedTestResult import SpeedTestResult


class DatabaseConnectionService:
    _instance = None

    @staticmethod
    def get_instance() -> DatabaseConnectionService:
        if DatabaseConnectionService._instance is None:
            DatabaseConnectionService()
        return DatabaseConnectionService._instance

    def __init__(self):
        if DatabaseConnectionService._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnectionService._instance = self

        self.connection = sqlite3.connect("saved.db")
        self.cursor = self.connection.cursor()

    def add_cellular_interface_signal(self, timestamp: int, cellular_interface_signal: CellularSignal, type: str):
        t = cellular_interface_signal
        self.cursor.execute("INSERT INTO cellular_interface_signal (timestamp, cellular_type, rssi, rsrp, rsrq, txpower, tac, bandinfo, mcc, mnc, status, enable) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (timestamp, type, t.rssi, t.rsrp, t.rsrq, t.txpower, t.tac, t.bandinfo, t.mcc, t.mnc,
                             t.status, t.enable))
        self.connection.commit()

    def add_cellular_interface_session(self, timestamp: int, duration: int, data_in: int, data_out: int):
        self.cursor.execute("INSERT INTO cellular_session (timestamp, duration, data_in, data_out) VALUES (?, ?, ?, ?)",
                            (timestamp, duration, data_in, data_out))
        self.connection.commit()

    def add_wan_status(self, timestamp: int, is_up: bool):
        self.cursor.execute("INSERT INTO is_wan_up (timestamp, is_up) VALUES (?, ?)", (timestamp, is_up))
        self.connection.commit()

    def add_display_network_type(self, timestamp: int, network_type: str):
        self.cursor.execute("INSERT INTO display_network_type (timestamp, cellular_type) VALUES (?, ?)", (timestamp, network_type))
        self.connection.commit()

    def add_internal_network_mode(self, timestamp: int, network_mode: str):
        self.cursor.execute("INSERT INTO internal_network_mode (timestamp, cellular_type) VALUES (?, ?)", (timestamp, network_mode))
        self.connection.commit()

    def add_cellular_signal_power_homepage(self, timestamp: int, rsrp: int):
        self.cursor.execute("INSERT INTO signal_power_homepage (timestamp, rsrp) VALUES (?, ?)", (timestamp, rsrp))
        self.connection.commit()

    def add_device(self, timestamp: int, device: Device):
        d = device
        self.cursor.execute("INSERT INTO device (timestamp, device_id, hostname, macaddress, ipaddress, type, link, lease, active, lastseen, ethernet, wireless, ipv6address) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (timestamp, d.id, d.hostname, d.macaddress, d.ipaddress, d.type, d.link, d.lease,
                             d.active, d.lastseen, json.dumps(d.ethernet), json.dumps(d.wireless), json.dumps(d.ip6address)))
        self.connection.commit()

    def add_speed_test(self, timestamp: int, speed_test_result: SpeedTestResult):
        r = speed_test_result
        self.cursor.execute("INSERT INTO speed_test (timestamp, download, upload, ping, byte_sent, byte_received, client_ip, server_name, server_city) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (timestamp, r.download, r.upload, r.ping, r.bytes_sent, r.bytes_received,
                             r.client.get("ip", ""), r.server.get("sponsor", ""), r.server.get("name", "")))
        self.connection.commit()

