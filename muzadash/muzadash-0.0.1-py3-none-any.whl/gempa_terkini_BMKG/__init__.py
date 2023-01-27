import requests
from bs4 import BeautifulSoup

def ekstraski_data():
    """
    Tanggal: 24 Januari 2023,
    Waktu: 23:10:22 WIB
    Magnitudo: 5.1
    Kedalaman: 50 km
    Lokasi: 3.49 LU - 128.62 BT
    Pusat gempa: 164 km TimurLaut DARUBA-MALUT
    Keterangan: tidak berpotensi TSUNAMI
    :return:
    """
    try:
        content = requests.get("https://bmkg.go.id")
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")
        result = soup.find("span", {"class": "waktu"})
        waktu = result.text.split(", ")
        jam = waktu[1]
        tanggal = waktu[0]

        result = soup.find("div", {"class": "col-md-6 col-xs-6 gempabumi-detail no-padding"})
        result = result.findChildren("li")
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        pusat = None
        keterangan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(" - ")
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                pusat = res.text
            elif i == 5:
                keterangan = res.text
            i = i + 1

        hasil = dict()
        hasil["tanggal"] = tanggal
        hasil["jam"] = jam
        hasil["magnitudo"] = magnitudo
        hasil["kedalaman"] = kedalaman
        hasil["koordinat"] = {"ls": ls, "bt": bt}
        hasil["lokasi"] = pusat
        hasil["keterangan"] = keterangan

        return hasil
    else:
        return None
def tampilkan_data(result):
    if result is None:
        print("Tidak bisa menemukan data gempa terkini")
        return

    print("Gempa Terakhir berdasarkan BMKG")
    print(f"Tanggal {result['tanggal']}")
    print(f"Jam {result['jam']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat: LS= {result['koordinat']['ls']}, BT= {result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"Keterangan {result['keterangan']}")

if __name__ == "__main__":
    result = ekstraski_data()
    tampilkan_data(result)