def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def hex_to_rgb(hex):
    return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def hex_to_csv(hex):
    return ','.join(str(x) for x in hex_to_rgb(hex))


def csv_to_hex(csv):
    return rgb_to_hex(tuple(int(x) for x in csv.split(',')))
