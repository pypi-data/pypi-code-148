import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command") # this line changed

    login_parser = subparsers.add_parser('login', help='Log in')
    login_parser.add_argument('-u', '--user', help='username')
    login_parser.add_argument('-t', '--token', help='login token')

    submit_parser = subparsers.add_parser('submit', help='Submit your code')
    submit_parser.add_argument('-f', '--file', help='Absolute path of your source code')

    args = parser.parse_args()

    return args
