from bs4 import BeautifulSoup

def get_all_images(filepath):
    soup = BeautifulSoup(open(filepath).read(), features="html.parser")
    images = soup.findAll("img")
    images_link = []
    for image in images:
        if "assets/" in image["src"]:
            images_link.append(image["src"])
    return images_link
