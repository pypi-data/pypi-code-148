from datetime import datetime


def dt_isoformat_to_ms(dt_isoformat: str) -> int:
    """Convert date in ISO format to ms since epoch"""
    return int(datetime.fromisoformat(dt_isoformat).timestamp() * 1000)


def dt_ms_to_isoformat(tm: int) -> str:
    """Convert date in ms since epoch to ISO format"""
    return datetime.fromtimestamp(int(tm) / 1000).isoformat()
