from bs4 import BeautifulSoup


def get_number_of_pages(soup: BeautifulSoup) -> int:
    try:
        page_select_button_text = soup.find(
            "select", {"id": "pageSelect"}).find("option").text
        number_of_pages = page_select_button_text.split("/")[-1]

        return number_of_pages
    except:
        return 0


def get_tickers_table(soup: BeautifulSoup) -> dict:

    headers = [item.text for item in soup.find_all(
        "td", {"class": ["table-top", "cursor-pointer"]})]
    table = [item.text for item in soup.find_all(
        "td", {"class": "screener-body-table-nw"})]

    return headers, table
