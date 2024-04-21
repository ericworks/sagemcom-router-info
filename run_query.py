from __future__ import annotations

import time
from math import ceil
from typing import List

from rq.Cellular import Cellular
from rq.CellularSignal import CellularSignal
from rq.CellularType import CellularType
from rq.Device import Device
from rq.RequestLibrary import get_devices, get_signal_power, get_cellular_session_info, is_wan_up, \
    get_display_network_type, get_internal_network_mode, get_cellular_interface_signal, get_connected_device_list
from rq.SpeedTestResult import SpeedTestResult
from sqlite_connector import DatabaseConnectionService
from test_speed import get_speedtest_result


def run(should_test_speed: bool = False):
    ts = int(time.time())
    devices:List[Device] = get_devices()
    for device in devices:
        DatabaseConnectionService.get_instance().add_device(ts, device)

    signal_power, unit = get_signal_power()
    DatabaseConnectionService.get_instance().add_cellular_signal_power_homepage(ts, signal_power)

    cellular:Cellular = get_cellular_session_info()
    DatabaseConnectionService.get_instance().add_cellular_interface_session(ts,
                                                                            cellular.get_session_duration_in_seconds(),
                                                                            cellular.get_data_in_byte(),
                                                                            cellular.get_data_out_byte())

    wan_up: bool = is_wan_up()
    DatabaseConnectionService.get_instance().add_wan_status(ts, wan_up)

    display_cellular_type:CellularType = get_display_network_type()
    DatabaseConnectionService.get_instance().add_display_network_type(ts, str(display_cellular_type))

    internal_network_mode:CellularType = get_internal_network_mode()
    DatabaseConnectionService.get_instance().add_internal_network_mode(ts, str(internal_network_mode))

    c_signal: CellularSignal = get_cellular_interface_signal(CellularType.t_5G_NSA)
    DatabaseConnectionService.get_instance().add_cellular_interface_signal(ts, c_signal, CellularType.t_5G_NSA.value)

    c_signal: CellularSignal = get_cellular_interface_signal(CellularType.t_4G)
    DatabaseConnectionService.get_instance().add_cellular_interface_signal(ts, c_signal, CellularType.t_4G.value)

    connected_devices: List[str] = get_connected_device_list()
    for device in connected_devices:
        DatabaseConnectionService.get_instance().add_connected_device(ts, device)

    if not should_test_speed:
        return

    speed_test_result: SpeedTestResult|None = None
    has_error = False
    attempts = 0
    while attempts < 3:
        try:
            speed_test_result: SpeedTestResult = get_speedtest_result()
            break
        except Exception as e:
            print("Speed test failed")
            print(e)
            has_error = True
            attempts += 1
            time.sleep(5)

    if speed_test_result is not None and not has_error:
        DatabaseConnectionService.get_instance().add_speed_test(ts, speed_test_result)
