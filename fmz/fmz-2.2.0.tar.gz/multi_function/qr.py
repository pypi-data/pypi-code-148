import qrcode


def makeqr(text: str, filename: str):
    try:
        img = qrcode.make(text)
        img.save(filename)
        return True
    except:
        return False