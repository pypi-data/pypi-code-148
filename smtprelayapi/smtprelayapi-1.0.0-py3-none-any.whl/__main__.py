from autoinject import injector
from .client import RelayClient


@injector.inject
def main_entry(rc: RelayClient = None):
    rc.retry_all()


if __name__ == "__main__":
    main_entry()
