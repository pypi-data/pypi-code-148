import requests
import xmltodict

# Data is by BCP GmbH under CC BY-NC 4.0 and it's here https://opendata.bonn.de/dataset/parkh%C3%A4user-und-parkpl%C3%A4tze-realtime-belegung


def get_data():
    """
    Get the xml data from the bcp bonn api and make the data to dictionarys
    """
    data_unformatted = requests.get(
        "https://www.bcp-bonn.de/stellplatz/bcpext.xml"
    ).content
    data = xmltodict.parse(data_unformatted)
    return data


def format_data(data):
    """
    Format the data so that we only have, what we need
    """
    end_data = []
    for i in data["parkhaeuser"]["parkhaus"]:
        end_data.append(
            {
                "id": i["lfdnr"],
                "title": i["bezeichnung"],
                "parking_spots_total": int(i["gesamt"]),
                "parking_spots_free": int(i["frei"]),
                "parking_spots_used": int(i["gesamt"]) - int(i["frei"]),
                "status": i["status"],
                "timestamp_time": i["zeitstempel"].split()[1],
                "timestamp_date": i["zeitstempel"].split()[0],
            }
        )
    return end_data
