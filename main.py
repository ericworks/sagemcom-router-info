import os
import time
import argparse
from dotenv import load_dotenv
from rq.RequestLibrary import get_auth_state
from rq.login import do_login
from rq.sessions import RequestSessionMgr
from run_query import run

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Collecting data from router and speed-test net')
    parser.add_argument('--username', type=str, help='username for login')
    parser.add_argument('--password', type=str, help='password for login')
    parser.add_argument('--should-test-speed', type=bool, help='should run speedtest', default=True)
    parser.add_argument("--speed-test-interval", type=int, help="speed test interval in minutes", default=3)
    parser.add_argument("--router-query-interval", type=int, help="speed test interval in seconds", default=90)
    parser.add_argument("--env-file", type=str, help="environment file path")
    args = parser.parse_args()

    if args.username is not None and args.password is not None:
        username = args.username
        password = args.password

    elif args.env_file is not None:
        load_dotenv(args.env_file)
        username = os.getenv("LOGIN_USERNAME")
        password = os.getenv("LOGIN_PASSWORD")

    else:
        load_dotenv()
        username = os.getenv("LOGIN_USERNAME")
        password = os.getenv("LOGIN_PASSWORD")

    if username is None or password is None or username == "" or password == "":
        raise Exception("Username or password is not provided")

    # check if speed test interval is less than 3 minutes
    if args.speed_test_interval is None or args.speed_test_interval < 3:
        raise Exception("Speed test interval should be at least 3 minutes")

    # check if router query interval is less than 1 minute
    if args.router_query_interval is None or args.router_query_interval < 60:
        raise Exception("Router query interval should be at least 60 seconds")

    print("Authenticating...")

    speed_test_wait_seconds = 0
    while True:

        do_login(username, password)
        if args.should_test_speed and speed_test_wait_seconds > int(args.speed_test_interval):
            should_run_speedtest = True
            speed_test_wait_seconds = 0
        else:
            should_run_speedtest = False

        run(should_test_speed=should_run_speedtest)

        RequestSessionMgr.get_instance().save_session_to_file()

        print("Sleeping...")
        time.sleep(args.router_query_interval)

        if args.should_test_speed:
            speed_test_wait_seconds += args.router_query_interval
