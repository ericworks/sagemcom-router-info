import json
from typing import List, Tuple
from requests import Response

from rq.Cellular import Cellular
from rq.CellularSignal import CellularSignal
from rq.CellularType import CellularType
from rq.common import common_headers, auth_state_url, device_url, cellular_url, rsrp_url, status_url, network_type_url, \
    set_cellular_mode_url, network_mode_url, reboot_url, cellular_interface_5g_url, cellular_interface_url, \
    connected_device_24_url, connected_device_5_url
from rq.Device import Device
from rq.filter_fields import filter_fields
from rq.login import do_login
from rq.sessions import RequestSessionMgr


class RequestLibraryException(Exception):
    pass


class RequestStatusCodeError(RequestLibraryException):
    pass


class ResponseFormatError(RequestLibraryException):
    pass


class SetCellularModeFailed(RequestLibraryException):
    pass


class RebootError(RequestLibraryException):
    pass


def _common_request_sender(url: str) -> Response:
    return RequestSessionMgr.get_session().get(url, headers=common_headers)


def _check_status_code(resp: Response, descriptor: str = ""):
    if resp.status_code >= 400 or resp.status_code < 200:
        raise RequestStatusCodeError(f"Request {descriptor} failed with status code {resp.status_code}")


def get_auth_state() -> bool:
    resp = _common_request_sender(auth_state_url)
    _check_status_code(resp, "auth state")
    result = json.loads(resp.text)[0]
    if result.get("authenticated", False):
        return True


def get_devices() -> List[Device]:
    resp = _common_request_sender(device_url)
    _check_status_code(resp, "devices")
    result = json.loads(resp.text)
    try:
        devices = result[0]["hosts"]["list"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for devices response")
    for device in devices:
        yield Device(**device)


def get_signal_power() -> Tuple[int, str]:
    resp = _common_request_sender(rsrp_url)
    _check_status_code(resp, "rsrp")
    result = json.loads(resp.text)
    try:
        rsrp = result["cellular"]["rsrp"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for rsrp response")
    return int(rsrp), "dBm"


def get_cellular_session_info() -> Cellular:
    resp = _common_request_sender(cellular_url)
    _check_status_code(resp, "cellular session")
    result = json.loads(resp.text)
    try:
        cellular = result[0]["cellular"]["session"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for cellular response")
    return Cellular(**cellular)


def is_wan_up() -> bool:
    resp = _common_request_sender(status_url)
    _check_status_code(resp, "wan status")
    result = json.loads(resp.text)
    try:
        status = result["status"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for status response")
    return True if status == "Up" else False


def get_display_network_type() -> CellularType:
    # 5G NSA
    resp = _common_request_sender(network_type_url)
    _check_status_code(resp, "network type")
    result = json.loads(resp.text)
    try:
        network_type = result["cellular"]["network_type"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for network type response")
    if network_type == "5G NSA":
        return CellularType.t_5G_NSA.value
    elif network_type == "4G":
        return CellularType.t_4G.value
    else:
        print("network type raw: " + network_type)
        return CellularType.DISCONNECT.value


def get_internal_network_mode() -> CellularType:
    resp = _common_request_sender(network_mode_url)
    _check_status_code(resp, "network mode")
    result = json.loads(resp.text)
    try:
        network_mode = result["cellular"]["interface"]["network_mode"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for network mode response")
    if network_mode == "5GNSA":
        return CellularType.t_5G_NSA.value
    elif network_mode == "4G":
        return CellularType.t_4G.value
    else:
        return CellularType.DISCONNECT.value


def put_network_mode(cellular_type: CellularType):
    c_type_str = CellularType.t_5G_NSA.value if cellular_type == CellularType.t_5G_NSA else CellularType.t_4G.value
    resp = RequestSessionMgr.get_session().put(set_cellular_mode_url, headers=common_headers, data={
        "mode": c_type_str
    })
    if resp.status_code < 200 or resp.status_code >= 400:
        raise SetCellularModeFailed("Failed to set cellular mode")


def get_cellular_interface_signal(cellular_type_to_query: CellularType) -> CellularSignal:
    cellular_signal_url = cellular_interface_url if cellular_type_to_query == CellularType.t_4G else cellular_interface_5g_url
    resp = _common_request_sender(cellular_signal_url)
    _check_status_code(resp, "cellular interface signal")
    result = json.loads(resp.text)
    try:
        interface = result[0]["cellular"]["interfaces"][0]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for network mode response")
    return CellularSignal(**filter_fields(CellularSignal, interface))


def post_reboot():
    resp = RequestSessionMgr.get_session().post(reboot_url, headers=common_headers, data={})
    if resp.status_code < 200 or resp.status_code >= 400:
        raise RebootError("Failed to set cellular mode")


def get_connected_device_list() -> List[str]:
    connected_devices = []
    resp_24 = _common_request_sender(connected_device_24_url)
    _check_status_code(resp_24, "connected devices 2.4G")
    result_24 = json.loads(resp_24.text)
    try:
        devices_24 = result_24[0]["hosts"]["list"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for connected devices 2.4G response")
    for device in devices_24:
        connected_devices.append(device["macaddress"])

    resp_5 = _common_request_sender(connected_device_5_url)
    _check_status_code(resp_5, "connected devices 5G")
    result_5 = json.loads(resp_5.text)
    try:
        devices_5 = result_5[0]["hosts"]["list"]
    except KeyError:
        raise ResponseFormatError("Response format error, check the response format for connected devices 5G response")
    for device in devices_5:
        connected_devices.append(device["macaddress"])

    return connected_devices


if __name__ == '__main__':
    do_login("admin", "password")
    # put_network_mode(CellularType.t_5G_NSA)
    print(get_connected_device_list())
    exit(0)
    print(list(get_devices()))
    exit(0)
    print(get_cellular_interface_signal(CellularType.t_5G_NSA))
    print(get_display_network_type())
    print(get_internal_network_mode())
    exit(0)
    print(is_wan_up())
