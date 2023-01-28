from .bcp_realtime import get_data, format_data
import time
import csv


class HistoryTracker:
    def __init__(self, time_to_repeat):
        self.time_to_repeat = time_to_repeat
        self.scheme = [
            "parking_spots_total",
            "parking_spots_free",
            "parking_spots_used",
            "time",
            "date",
        ]
        if self.time_to_repeat < 60:
            raise Exception("The time to repeat is below 60.\nThis would spam the api.")

    def track_history_csv(self):
        data = get_data()
        data = format_data(data)
        for i in data:
            with open(f'{i["title"]}.csv', "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.scheme)
                writer.writeheader()
        while True:
            data = get_data()
            data = format_data(data)
            for i in data:
                with open(f'{i["title"]}.csv', "a", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.scheme)
                    writer.writerow(
                        {
                            "parking_spots_total": int(i["parking_spots_total"]),
                            "parking_spots_free": int(i["parking_spots_free"]),
                            "parking_spots_used": int(i["parking_spots_used"]),
                            "time": i["timestamp_time"],
                            "date": i["timestamp_date"],
                        }
                    )
            time.sleep(self.time_to_repeat)
