import pandas as pd
from io import BytesIO
from extcolors import extract_from_path
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import extcolors
import altair as alt
import os
import re
import requests


def check_param_validity(url, tolerance, limit):
    """
    Checks if the input params are valid

    Parameters
    ----------
    img_url: str
        the url of the image from which the color palette is to be extracted
    tolerance: int
        a value between 0 and 100 representing the tolerance level for color matching
    limit: int
        the maximum number of colors to be returned in the palettel

    Returns:
    -------
    bool:
        True if params are valid else return False
    """

    # Regex from https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/

    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return (
        re.search(regex, url) is not None
        and (tolerance >= 0 and tolerance <= 100)
        and (limit >= 0 and limit <= 100)
    )


def rgb_to_hex(rgb):
    """
    Convert an RGB value stored as a tuple to a hex color code.

    Parameters
    ----------
    rgb : tuple
        The tuple of integers representing the RGB values
    Returns
    -------
    str
        The hex color code of the input RGB color.
    """

    return "#" + "".join(
        ["0{:x}".format(v) if v < 16 else "{:x}".format(v) for v in rgb]
    )


def get_color_palette(img_url, tolerance, limit):
    """
    Gets the color palette of an image

    Extracts the most common colors from an image
    and returns them as a dataframe of hex color codes and RGB values

    Parameters
    ----------
    img_url: str
        the url of the image from which the color palette is to be extracted
    tolerance: int
        a value between 0 and 100 representing the tolerance level for color matching
    limit: int
        the maximum number of colors to be returned in the palette

    Returns
    ----------
    dataframe
        a dataframe of hex color codes and RGB values corresponding to the most common colors in the image

    Examples
    --------
    get_color_palette('https://i.imgur.com/s9egWBB.jpg', 20, 5)
    """

    if not check_param_validity(img_url, tolerance, limit):
        print("The input parameters are not valid")
        return

    temp_image_name = "image_for_extraction.jpg"
    temp_image_storage_path = r"./images"
    full_file_path = os.path.join(temp_image_storage_path, temp_image_name)
    resize_large_img = 1000

    # Send a GET request to the URL and get the image data
    try:
        response = requests.get(img_url, timeout=30)

    except requests.exceptions.ConnectionError:
        raise Exception(
            "There seems to be an error accessing the URL and downloading it as an image. Please check the URL and try again."
        )

    if not response.status_code == 200:
        raise Exception(response.reason)
        
    try:
        image = Image.open(BytesIO(response.content))

        if response.status_code != 200:
            raise Exception("Unable to get image from the web url.")

    except PIL.UnidentifiedImageError:
        raise Exception("The URL may not point to an image. Please check the URL and try again.")

    image.thumbnail((resize_large_img, resize_large_img))
    image.name = temp_image_name
    image.seek(0)

    # Make necessary directories to the required path
    if not os.path.exists(temp_image_storage_path):
        os.makedirs(temp_image_storage_path)

    image.save(full_file_path)

    colors, _ = extract_from_path(full_file_path, tolerance=tolerance, limit=limit)

    df = pd.DataFrame(columns=["HEX", "RGB"])
    data = {
        "HEX": [rgb_to_hex(rgb_value) for rgb_value in [color[0] for color in colors]],
        "RGB": [
            ",".join(map(str, rgb_value))
            for rgb_value in [color[0] for color in colors]
        ],
        "Color Count": [freq for freq in [color[1] for color in colors]],
    }
    df = pd.DataFrame(data)

    # Clean Up
    os.remove(full_file_path)

    return df


def donut(img_url, num_clrs, tolerance, img_size, plot_show=True):
    """Create a donut chart of the top n colors in the image (number of colors specified by the user)

    Creates a square donut chart using the n most common colors from the image

    Parameters
    ----------
    img_url: str
        the url of the image that the user is pulling the colors from
    num_clrs: int
        the number of colors the user wants to pull from the image
    tolerance: int
        a value between 0 and 100 representing the tolerance level for color matching
    img_size: int
        the pixel width and height of the resulting chart
    plot_show: bool
        set False to supress output of the chart

    Returns
    ----------
    matplotlib.figure.Figure
        Donut chart of the colours

    Examples
    --------
    donut('https://i.imgur.com/s9egWBB.jpg', 5, 20, 400)
    """

    # get the top 100 colors and their proportion in the image
    df = get_color_palette(img_url, tolerance, limit=100)
    colors_prop = [
        round(x / sum(df["Color Count"].to_list()), 2)
        for x in df["Color Count"].to_list()
    ]

    img_colors = df["HEX"].to_list()[0:num_clrs]
    img_colors.append("#a9a9a9")

    value = colors_prop[0:num_clrs]
    value.append(round(1 - sum(value), 2))

    # need to do this to keep the donut hole in order
    factor = 0  # initialize the factor
    img_size = img_size / 227  # macbook air resolution is 227 pixels/inch
    if img_size > 600 / 227:
        factor = 0.3
    elif img_size <= 200 / 227:
        factor = 0.7
    elif img_size <= 400 / 227:
        factor = 0.6
    elif img_size <= 600 / 227:
        factor = 0.4

    category_value = []
    for i in range(len(img_colors)):
        category_value.append(img_colors[i] + ": " + str(f"{value[i]*100:.0f}%"))

    # create the donut hole
    pie = plt.Circle((0, 0), radius=img_size * factor, color="white")

    # make labels
    labels = category_value[:-1]
    labels.append("Other colors: " + str(f"{value[-1]*100:.0f}%"))

    # label and color
    plt.pie(value, labels=labels, colors=img_colors, radius=img_size)
    p = plt.gcf()
    p.gca().add_artist(pie)

    if plot_show:
        plt.show()
        return
    return p


def scatterplot(img_url, dataset, x, y, fill, tolerance=50):
    """Create a two-dimensional scatterplot based on the colours of the image

    Creates a simple scatterplot using the colours selected from the image,
    plotting two features from a dataset of the users choosing.

    Parameters
    ----------
    img_url : str
        url of the image to extract colours
    dataset : pandas.DataFrame
        the dataset to plot (already imported)
    x: str
        the data to plot on the x-axis
    y: str
        the data to plot on the y-axis
    fill: str
        the data to use to fill in the points of the scatter plot
    tolerance : int
        number between 0 and 100 used to give better visual representation;
        0 will not group any similar colours together, 100 will group all colours into one

    Returns
    ----------
    altair.vegalite.v4.api.Chart
        Scatterplot using image colours

    Examples
    --------
    scatterplot('https://i.imgur.com/s9egWBB.jpg', penguins, 'bill_length_mm', 'body_mass_g', 'species', 50)
    """
    if not img_url.startswith("https://"):
        raise ValueError("'img_url' must be a link (not a path).")

    if not [ext for ext in [".png", ".jpg", ".jpeg"] if (ext in img_url)]:
        raise ValueError("'img_url' must be a direct link to an image file.")

    if not isinstance(dataset, pd.core.frame.DataFrame):
        raise TypeError("'dataset' must be a pandas DataFrame.")

    if not isinstance(x, str):
        raise TypeError("'x' must be a string value.")

    if not isinstance(y, str):
        raise TypeError("'y' must be a string value.")

    if not isinstance(fill, str):
        raise TypeError("'y' must be a string value.")

    if not 0 <= tolerance <= 100:
        raise ValueError("'tolerance' must be between 0 and 100.")

    # Get image colour palette
    colours = get_color_palette(img_url, tolerance, dataset[fill].nunique())

    # Make Scatterplot based of the image colour palette
    scatter = (
        alt.Chart(dataset)
        .mark_point()
        .encode(
            alt.X(field=x),
            alt.Y(field=y),
            alt.Fill(field=fill, scale=alt.Scale(range=colours["HEX"].to_list())),
        )
    )
    return scatter


def negative(img_url, num_colours=1, tolerance=0):
    """Invert top n colours in an image file.

    Colours are extracted from an image via URL and reversed,
    (e.g. red becomes cyan, green becomes magenta, yellow becomes blue)
    then stored in a table as HEX codes and RGB values.

    Parameters
    ----------
    img_url : str
        URL of an image file
    num_colours : int
        number of colours to be extracted
    tolerance : int
        number between 0 and 100 used to give better visual representation;
        0 will not group any similar colours together, 100 will group all colours into one

    Returns
    -------
    pandas.DataFrame
        a table of the top n inverted colours in the image, including their HEX codes and RGB values

    Examples
    --------
    >>> negative("https://i.imgur.com/s9egWBB.jpg", 3, 20)
    """
    if not img_url.startswith("https://"):
        raise ValueError("'img_url' must be a link (not a path).")

    if not [ext for ext in [".png", ".jpg", ".jpeg"] if (ext in img_url)]:
        raise ValueError("'img_url' must be a direct link to an image file.")

    if not isinstance(num_colours, int):
        raise TypeError("'num_colours' must be an integer value.")

    if not isinstance(tolerance, int):
        raise TypeError("'tolerance' must be an integer value.")

    if not 0 <= tolerance <= 100:
        raise ValueError("'tolerance' must be between 0 and 100.")

    # Load image
    try:
        img = Image.open(BytesIO(requests.get(img_url, stream=True).content))
   
    except PIL.UnidentifiedImageError:
        raise Exception("URL has not been read. Try another URL.")

    # Resize image for processing - 800 pixel maximum
    width = 800 / float(img.size[0])
    height = int((float(img.size[1]) * float(width)))
    img = img.resize((800, height), Image.LANCZOS)

    # Extract colours
    colours, pixel_count = extcolors.extract_from_image(
        img, tolerance=tolerance, limit=num_colours
    )

    # Check if there are any non-transparent pixels
    if not colours:
        raise ValueError(
            "No coloured pixels detected in the image. It is likely transparent or something went wrong."
        )

    # Format RGB codes into list
    colour_list = str(colours).replace("[(", "").split(", (")
    rgb_list = [i.split("), ")[0] + ")" for i in colour_list]

    # Inverse RGB colour codes and extract HEX codes
    inversed_rgb = []
    hex = []
    for cols in rgb_list:
        rgb = cols.replace("(", "").replace(")", "").split(", ")
        inverse_code = (255 - int(rgb[0]), 255 - int(rgb[1]), 255 - int(rgb[2]))
        inversed_rgb.append(inverse_code)
        hex.append("#%02x%02x%02x" % inverse_code)

    # Format data frame
    df = pd.DataFrame({"HEX": hex, "RGB": inversed_rgb})

    return df
