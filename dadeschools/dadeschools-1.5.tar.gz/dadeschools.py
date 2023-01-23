
import requests
from bs4 import BeautifulSoup as bs


def main():
    # url = 'https://mdcpsportalapps2.dadeschools.net/PIVredirect/?ID={StudentID}'

    id_number = input("Enter your ID number: ")

    get_student_id_url = f'https://mdcpsportalapps2.dadeschools.net/PIVredirect/?ID={id_number}'

    #~ Testing

    # Get StudentID
    r = requests.get(get_student_id_url)
    StudentID = r.text.split("value='")[2].split("'")[0]

    url = 'https://gradebook.dadeschools.net/Pinnacle/Gradebook/Link.aspx?target='

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'action': 'trans',
        'StudentID': StudentID
    }

    cookie = requests.get(url, headers=headers, data=data).headers['Set-Cookie']

    url = "https://gradebook.dadeschools.net/Pinnacle/Gradebook/InternetViewer/GradeReport.aspx"

    headers = {
        'Referer': get_student_id_url,
        'Cookie': cookie,
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.0.0 Safari/537.36'
    }

    r = requests.get(url, headers=headers)

    soup = bs(r.content, 'html.parser')

    # grades = [(div.text.strip(), div.nextSibling.nextSibling.text) for div in soup.find_all('div', {'class': 'letter'})]

    # for grade in grades:
    #     print(grade[0].replace("\t", "").replace("\r", "").replace("\n", ""))

    # grades = [
    #     (
    #         a['aria-label'], 
    #         "None" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0], 
    #         "" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0]
    #     )
    #     for a in soup.find_all('a', {'class': 'letter-container'})
    # ]

    first = []
    second = []
    third = []
    fourth = []

    for a in soup.find_all('a', {'class': 'letter-container'}):
        if a['aria-label'].startswith("1"):
            first.append(
                (
                    a['aria-label'].split(" - ")[-1], 
                    "No grade" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0], 
                    "" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0]
                )
            )
        if a['aria-label'].startswith("2"):
            second.append(
                (
                    a['aria-label'].split(" - ")[-1], 
                    "No grade" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0], 
                    "" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0]
                )
            )
        if a['aria-label'].startswith("3"):
            third.append(
                (
                    a['aria-label'].split(" - ")[-1], 
                    "No grade" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0], 
                    "" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0]
                )
            )
        if a['aria-label'].startswith("4"):
            fourth.append(
                (
                    a['aria-label'].split(" - ")[-1], 
                    "No grade" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("<div>")[1].split("<span")[0], 
                    "" if str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0] == '' else str(list(a.descendants)[-11]).replace("\t", "").replace("\r", "").replace("\n", "").split("percent\">")[1].split("</span>")[0]
                )
            )

    print("\n1ST GRADING QUARTER")
    for grade in first:
        print("\t", grade[0], "|", grade[1], grade[2])

    print("\n2ND GRADING QUARTER")
    for grade in second:
        print("\t", grade[0], "|", grade[1], grade[2])

    print("\n3RD GRADING QUARTER")
    for grade in third:
        print("\t", grade[0], "|", grade[1], grade[2])

    print("\n4TH GRADING QUARTER")
    for grade in fourth:
        print("\t", grade[0], "|", grade[1], grade[2])


main()
