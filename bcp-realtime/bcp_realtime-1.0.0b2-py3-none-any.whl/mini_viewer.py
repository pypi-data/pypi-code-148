import time

from .bcp_realtime import get_data, format_data


def run_mini_viewer():
    data = get_data()
    data = format_data(data)

    print(
        "IMPORTANT: Data is by BCP GmbH and is under CC BY-NC 4.0\nIt can be found here: https://opendata.bonn.de/dataset/parkh%C3%A4user-und-parkpl%C3%A4tze-realtime-belegung"
    )
    print(f"Time: {data[0]['timestamp_time']}")
    print(f"ID  |  Title  | Total | Free | Used | Status")

    for i in data:
        print(
            f"{i['id']} | {i['title']} | {i['parking_spots_total']} | {i['parking_spots_free']} | {i['parking_spots_used']} | {i['status']}"
        )
