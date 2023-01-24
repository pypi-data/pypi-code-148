import requests
from bs4 import BeautifulSoup

def get_hacknsun_counter(year, session):
    page = requests.get(f"https://ticdesk.teckids.org/app/paweljong/event/hacknsun-{year}-bn-{session}")
    soup = BeautifulSoup(page.content, 'html.parser')
    info_block = soup.find('div', class_="col s12")
    content = info_block.find_all('tr')
    content = content[3].find_all('td')[1]
    content = str(content)
    return int(content.replace("<td>", "").replace("</td>", ""))
