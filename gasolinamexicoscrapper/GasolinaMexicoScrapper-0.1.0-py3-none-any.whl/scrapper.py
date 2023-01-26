import requests
import locale
from bs4 import BeautifulSoup
from datetime import datetime
from .exceptions import ServiceError, NotFound

BASE_URL = "https://gasolinamexico.com.mx/"
STATE_URL = f"{BASE_URL}estados/"
STATION_URL = f"{BASE_URL}estacion/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/100.0.4896.75 Safari/537.36"
STATION_INFO_MAPPING = {
    "Razón Social:": "business_name",
    "Ubicación:": "address",
    "Permiso:": "license",
    "Teléfono:": "phone",
    "Página web:": "website",
    "Facturación:": "billing",
}


def fetch_page(url):
    headers = {
        "User-Agent": USER_AGENT
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 404:
            raise NotFound
        elif response.status_code != 200:
            raise ServiceError()
    except Exception as e:
        raise ServiceError(str(e))

    return response.text


def parse_date(date_string):
    raw_date = date_string.text.replace("Actualizados al ", "")
    return datetime.strptime(raw_date.lower(), '%d de %B de %Y')


def build_slug(url, page_url, kind):
    if kind == 'town':
        return {
            "slug": url.replace(page_url, '').replace('/', '')
        }
    if kind == 'station':
        id, slug, _ = url.replace(STATION_URL, '').split("/")
        return {
            "id": id,
            "slug": slug,
        }
    return {}


def extract_updated_date(soup):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    updated_date = soup.find('h3', class_="description")

    updated_date = parse_date(date_string=updated_date) if updated_date is not None else None

    return str(updated_date.date())


def extract_station_geolocation(soup):
    scripts = list(
        map(
            lambda item: item.text,
            soup.find_all('script')
        )
    )
    filter_scripts = list(
        filter(
            lambda text: "var map" in text,
            scripts
        )
    )
    geolocation = []
    for script in filter_scripts:
        geo_tags = script.split("var map = L.map('map').setView([")[1].strip()
        geo_tags = geo_tags.split("],")[0].strip().split(",")
        geolocation.append(
            {
                "latitud": geo_tags[0],
                "longitud": geo_tags[1],
            }
        )

    return geolocation


def extract_items_geolocation(soup):
    scripts = list(
        map(
            lambda item: item.text,
            soup.find_all('script')
        )
    )
    filter_scripts = list(
        filter(
            lambda text: "var stations" in text,
            scripts
        )
    )
    geolocation = []
    for script in filter_scripts:
        geo_tags = script.split("var stations = ")[1].strip()
        geo_tags = geo_tags.split(";")[0].strip()
        geolocation += eval(geo_tags)

    return geolocation


def find_station_geolocation(search_key, locations):
    filter_locations = list(
        filter(
            lambda l: search_key.upper() == l[0].upper(),
            locations
        )
    )
    for location in filter_locations:
        return {
            "latitud": location[1],
            "longitud": location[2],
        }
    return {}


def extract_station_price(soup):
    prices = []
    container = soup.find('div', id="average")
    if container is not None:
        prices = list(
            map(
                lambda card: {
                    "type": card.find('h2').text,
                    "price": card.find('p').text.replace('$', ''),
                },
                container.find_all('div', class_='card')
            )
        )

    return prices


def extract_station_info(soup):
    info = {}
    container = soup.find('div', class_='card-body')
    if container is not None:
        items = container.find('ul', class_="list-unstyled")
        if items is not None:
            for item in items.find_all('li'):
                raw_key = item.find('strong').text
                value = item.text.replace(raw_key, "").strip()
                key = STATION_INFO_MAPPING.get(raw_key, None)
                if key is not None:
                    info.update(
                        {
                            key: value
                        }
                    )
    return info


def extract_average_price(soup):
    average_container = soup.find('div', id="average")
    average_price = list(
        map(
            lambda card: {
                "type": card.find('h2').text,
                "price": card.find('p').text.replace('$', ''),
            },
            average_container.find_all('div', class_='card')
        )
    ) if average_container is not None else []

    return average_price


def extract_price_listing(soup, item_name, page_url=None, include_address=False):
    prices = soup.find('table', id="datatable").find('tbody').find_all('tr')

    return list(
        map(
            lambda item: {
                item_name: {
                    "name": item.find('a').text,
                    "url": item.find('a').attrs.get('href', ''),
                    **(
                        build_slug(url=item.find('a').attrs.get('href', ''), page_url=page_url, kind=item_name)
                    ),
                    **({
                           "address": item.find_all('td')[4].text,
                       }
                       if include_address else {}
                       ),
                },
                "magna": item.find_all('td')[1].text.replace("$", ""),
                "premium": item.find_all('td')[2].text.replace("$", ""),
                "disel": item.find_all('td')[3].text.replace("$", ""),
            },
            prices
        )
    )


def get_states():
    """
    This function fetch the state list from the data source and scrap it to format on a list of dicts formatted
    as follow.

    {
        "name": String,
        "url": String,
        "slug": String
    }

    :return: List of Dicts
    """
    html_content = fetch_page(url=STATE_URL)
    soup = BeautifulSoup(markup=html_content)

    links = soup.find_all('a')

    states_links = list(
        filter(
            lambda item: STATE_URL != item.attrs.get('href', '') and item.attrs.get('href', '').startswith(STATE_URL),
            links
        )
    )

    states = list(
        map(
            lambda item: {
                "name": item.text,
                "url": item.attrs.get('href'),
                "slug": item.attrs.get('href').replace(STATE_URL, "").replace("/", ""),
            },
            states_links
        )
    )

    return states


def get_state(state):
    """
    Function that fetch the average pricing and list of town on the state with the average prices for each town.

    If the state parameter match with more that one state, the function will return the first state fetched

    Format of the return dictionary

    {
        "update_date": String [Format YYYY-DD-MM],
        "average_price: List of Dict [{"type": String, "price": String [Format 00.00, empty string for No value]}],
        "towns": List of Dicts
        [
            {
            "town": dict{"name": String, "url": String, "slug": String} ,
            "magna": String,
            "premium": String,
            "disel": String
            }
        ]
    }

    :param state: String with the name of the state or the slug of the state
    :return: Dict or None if not found
    """
    states = get_states()
    filter_states = list(
        filter(
            lambda item: state.upper() == item['name'].upper() or state.upper() == item['slug'].upper(),
            states
        )
    )
    for fetch_state in filter_states:
        url = fetch_state['url']
        html_content = fetch_page(url=url)
        soup = BeautifulSoup(markup=html_content)

        updated_date = extract_updated_date(soup=soup)
        average_price = extract_average_price(soup=soup)
        price_listing = extract_price_listing(soup=soup, page_url=url, item_name="town")

        return {
            "update_date": updated_date,
            "average_price": average_price,
            "towns": price_listing,
        }


def get_town(state, city):
    """
    Function that fetch the average gas price for a given town within a state, also returns a list of all gas stations
    with in the town with the current gas prices, address and geolocation


    :param state: String
    :param city: String
    :return: Dict
    {
        "average_price": List of Dicts,
        "stations": List of Dicts
    }
    """
    state_data = get_state(state=state)
    if state_data is not None:
        filter_towns = list(
            filter(
                lambda item: city.upper() == item['town']['name'].upper() or city.upper() == item['town'][
                    'slug'].upper(),
                state_data.get('towns', [])
            )
        )

        for town in filter_towns:
            url = town['town']['url']
            html_content = fetch_page(url=url)
            soup = BeautifulSoup(markup=html_content)

            average_price = extract_average_price(soup=soup)
            price_listing = extract_price_listing(soup=soup, page_url=url, item_name="station", include_address=True)

            geolocations = extract_items_geolocation(soup=soup)

            price_listing = list(
                map(
                    lambda station: {
                        **station,
                        **(find_station_geolocation(station['station']['name'], geolocations))
                    },
                    price_listing
                )
            )

            return {
                "average_price": average_price,
                "stations": price_listing,
            }


def get_station(state, city, id=None, name=None):
    """
    Function that fetch a station detail, searched by a given id or a given name,

    the station is search on the given city that belong to the given state

    :param state: String
    :param city: String
    :param id: String
    :param name: String
    :return: Dict
    {
        "info": Dict,
        "prices": List of Dicts
    }
    """
    town = get_town(state=state, city=city)
    stations = list(
        filter(
            lambda station: id == station['station']['id'] or name == station['station']['name'],
            town['stations']
        )
    )

    for station in stations:
        url = station['station']['url']
        html_content = fetch_page(url=url)
        soup = BeautifulSoup(markup=html_content)

        prices = extract_station_price(soup)
        station_info = extract_station_info(soup)
        geo_location = extract_station_geolocation(soup)
        if len(geo_location) > 0:
            station_info.update(geo_location)

        return {
            "prices": prices,
            "info": station_info
        }
