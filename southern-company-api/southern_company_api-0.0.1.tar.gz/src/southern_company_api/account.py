import dataclasses
import datetime
import json
from typing import List

import aiohttp

from src.southern_company_api.company import Company


@dataclasses.dataclass
class DailyEnergyUsage:
    date: datetime.datetime
    usage: float
    cost: float
    low_temp: float
    high_temp: float


@dataclasses.dataclass
class HourlyEnergyUsage:
    time: datetime.datetime
    usage: float
    cost: float
    temp: float


class Account:
    def __init__(self, name: str, primary: bool, number: str, company: Company):
        self.name = name
        self.primary = primary
        self.number = number
        self.company = company

    async def get_service_point_number(self, jwt: str) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {jwt}"}
            # TODO: Is the /GPC for all customers or just GA power?
            try:
                async with session.get(
                    f"https://customerservice2api.southerncompany.com/api/MyPowerUsage/"
                    f"getMPUBasicAccountInformation/{self.number}/GPC",
                    headers=headers,
                ) as resp:
                    service_info = await resp.json()
                    # TODO: Test with multiple accounts
                    return service_info["Data"]["meterAndServicePoints"][0][
                        "servicePointNumber"
                    ]
            except aiohttp.ClientConnectorError as e:
                raise Exception(f"Failed to connect to api {e}")

    async def get_daily_data(
        self, start_date: datetime.datetime, end_date: datetime.datetime, jwt: str
    ) -> List[DailyEnergyUsage]:
        """Available 24 hours after"""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {jwt}"}
            params = {
                "accountNumber": self.number,
                "startDate": start_date.strftime("%m/%d/%Y 12:00:00 AM"),
                "endDate": end_date.strftime("%m/%d/%Y 12:00:00 AM"),
                "OPCO": self.company.name,
                "ServicePointNumber": await self.get_service_point_number(jwt),
                "intervalBehavior": "Automatic",
            }
            print(params)
            async with session.get(
                f"https://customerservice2api.southerncompany.com/api/MyPowerUsage/"
                f"MPUData/{self.number}/Daily",
                headers=headers,
                params=params,
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Failed to get JWT: {resp.status} {await resp.text()} "
                        f"{headers}"
                    )
                else:
                    response = await resp.json()
                    data = json.loads(response["Data"]["Data"])
                    day_maps = {}
                    dates = [date for date in data["xAxis"]["labels"]]
                    high_temps = [
                        temp["y"] for temp in data["series"]["highTemp"]["data"]
                    ]
                    low_temps = [
                        temp["y"] for temp in data["series"]["lowTemp"]["data"]
                    ]
                    for i, date in enumerate(dates):
                        day_maps[date] = DailyEnergyUsage(
                            date=datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"),
                            usage=-1,
                            cost=1,
                            low_temp=low_temps[i],
                            high_temp=high_temps[i],
                        )
                    # TODO: Zip weekday and weekend to make it simpler.
                    for weekend_cost in data["series"]["weekdayCost"]["data"]:
                        day_maps[weekend_cost["name"]].cost = weekend_cost["y"]
                    for weekend_usage in data["series"]["weekdayUsage"]["data"]:
                        day_maps[weekend_usage["name"]].usage = weekend_usage["y"]
                    for weekday_cost in data["series"]["weekdayCost"]["data"]:
                        day_maps[weekday_cost["name"]].cost = weekday_cost["y"]
                    for weekday_usage in data["series"]["weekdayUsage"]["data"]:
                        day_maps[weekday_usage["name"]].usage = weekday_usage["y"]
                    return list(day_maps.values())

    async def get_hourly_data(
        self, start_date: datetime.datetime, end_date: datetime.datetime, jwt: str
    ) -> List[HourlyEnergyUsage]:
        """Available 24 hours after"""
        if (end_date - start_date).days > 35:
            raise Exception("You cannot pass a date range greater than 35 days.")
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {jwt}"}
            params = {
                "accountNumber": self.number,
                "startDate": start_date.strftime("%m/%d/%Y 12:00:00 AM"),
                "endDate": end_date.strftime("%m/%d/%Y 12:00:00 AM"),
                "OPCO": self.company.name,
                "ServicePointNumber": await self.get_service_point_number(jwt),
                "intervalBehavior": "Automatic",
            }
            print(params)
            async with session.get(
                f"https://customerservice2api.southerncompany.com/api/MyPowerUsage/"
                f"MPUData/{self.number}/Hourly",
                headers=headers,
                params=params,
            ) as resp:
                if resp.status != 200:
                    raise Exception(
                        f"Failed to get JWT: {resp.status} {await resp.text()} "
                        f"{headers}"
                    )
                else:
                    data = await resp.json()
                    if data["Data"]["Data"] is None:
                        raise Exception("Received no data back for usage.")
                    data = json.loads(data["Data"]["Data"])
                    times = [
                        datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
                        for date in data["xAxis"]["labels"]
                    ]
                    costs = [cost["y"] for cost in data["series"]["cost"]["data"]]
                    usage = [usage["y"] for usage in data["series"]["usage"]["data"]]
                    temps = [temp["y"] for temp in data["series"]["temp"]["data"]]
                    hourly_usage = []
                    for i in range(len(times)):
                        hourly_usage.append(
                            HourlyEnergyUsage(
                                time=times[i],
                                cost=costs[i],
                                usage=usage[i],
                                temp=temps[i],
                            )
                        )
                    return hourly_usage
