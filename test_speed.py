import speedtest

from rq.SpeedTestResult import SpeedTestResult
from rq.filter_fields import filter_fields


def get_speedtest_result() -> SpeedTestResult:
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    return SpeedTestResult(**filter_fields(SpeedTestResult, s.results.dict()))


if __name__ == '__main__':
    print(get_speedtest_result())
