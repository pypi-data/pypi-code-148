import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


def sitesDrawer(postitions, color_dict={}, edge_color_dict={}, axis="NotGiven"):
    """
    draws sites on the canvas on the required position
    positions, list of tuples: the positions of the sites
    color_dict, dict: contains the colors of every individual site
    edge_color_dict, dict: contains the edge color of every individual site
    axis, pyplot.axes object: the axis to draw the figure on, default Nonegiven, will just draw it on a new figure
    """

    if axis == "NotGiven":
        fig, axis = plt.subplots()
    for index, position in enumerate(postitions):
        if index in color_dict.keys():
            color = color_dict[index]
        else:
            color = "white"
        if index in edge_color_dict.keys():
            edgecolor = edge_color_dict[index]
        else:
            edgecolor = "black"
        rectangle = plt.Rectangle(
            position,
            0.3,
            0.3,
            facecolor=color,
            edgecolor=edgecolor,
            lw=1.5,
            fill=True,
            zorder=5,
        )
        axis.add_patch(rectangle)


def colorDomains(domains):
    """
    Will read in the domains and give the right colorscheme
    domains, list of tuples: the domains of interest
    """
    pallete = sns.color_palette("pastel")
    colordict = {}
    for index, domain in enumerate(domains):
        for site in domain:
            colordict[site] = pallete[index]

    return colordict


def edgeColorDomains(domains):
    """
    Will read in the domains and give the right edgecolorscheme
    domains, list of tuples: the domains of interest
    """
    pallete = sns.color_palette()
    colordict = {}
    for index, domain in enumerate(domains):
        for site in domain:
            colordict[site] = pallete[index]

    return colordict


def lineDrawer(position_pairs, linecolor_dict={}, axis="NotGiven"):
    """
    Will draw lines on a figure.
    position_pairs, list of lists: contains all the pairs between which you want to draw a line.
    linecolor_dict, dict: contains the colors of each line
    axis, pyplot.axes object: the axis on which to make the drawing, if NotGiven, will make a new drawing

    note:
    If the drawing is circular, the position_pairs needs to end with the same point as it started
    example: [[point1, point2], [point2, point3], ... , [pointX, point1]]
    """
    if axis == "NotGiven":
        fig, axis = plt.subplots()
    for index, pair in enumerate(position_pairs):
        if index in linecolor_dict.keys():
            color = linecolor_dict[index]
        else:
            color = "black"
        axis.plot(
            (pair[0][0] + 0.15, pair[1][0] + 0.15),
            (pair[0][1] + 0.15, pair[1][1] + 0.15),
            color=color,
            zorder=0,
        )


def drawElectrons(alpha_pos, beta_pos, axis="NotGiven"):
    """
    Will draw the electrons in the right position
    alpha_pos, list of tuples: the postitions of the alpha electrons
    beta_pos, liest of tuples: the postitions of the beta electrons
    axis, pyplot.axes object: the axis on which the electrons need to be drawn, if NotGiven make a new image
    """
    if axis == "NotGiven":
        fig, axis = plt.subplots()

    for position in alpha_pos:
        axis.arrow(
            position[0] + 0.1,
            position[1] + 0.05,
            0,
            0.20,
            zorder=10,
            color="black",
            head_width=0.07,
            length_includes_head=True,
            head_length=0.05,
        )
    for position in beta_pos:
        axis.arrow(
            position[0] + 0.2,
            position[1] + 0.2 + 0.05,
            0,
            -0.20,
            zorder=10,
            color="black",
            head_width=0.07,
            length_includes_head=True,
            head_length=0.05,
        )


def plotONVs(
    pos_dict: dict,
    ONV_list: list,
    legend: list,
    edge_color_dict: dict = None,
    title: str = None,
) -> None:
    """
    plots ONVs for figure legends

    input
    :param pos_dict: site positions on the canvas
    :param ONV_list: list of ONVs, [[[alpha positions], [beta positions]], ...]
    :param legend: a list containing colors and markers used in the plot [(color, marker), ...]
    :param edge_color_dict: dict containing edge color for each site, if None, edge_color will be black
    :param title: the plot title, if None the plot will not be saved
    """
    fig, ax = plt.subplots(len(ONV_list) // 3 + 1, 3, figsize=(10, 7))
    ax = ax.flatten()
    for index, ONV in enumerate(ONV_list):
        axis = ax[index]
        sitesDrawer(
            [pos_dict[i] for i in range(len(pos_dict.keys()))],
            edge_color_dict=edge_color_dict,
            axis=axis,
        )
        lineDrawer([(pos_dict[i], pos_dict[i + 1]) for i in range(2)], axis=axis)
        alphas = ONV[0]
        betas = ONV[1]
        alpha_pos = [pos_dict[pos] for pos in alphas]
        beta_pos = [pos_dict[pos] for pos in betas]
        drawElectrons(alpha_pos=alpha_pos, beta_pos=beta_pos, axis=axis)
        axis.plot(0.5, 0.4, marker=legend[index][1], color=legend[index][0])

    for axis in ax:
        axis.axis("off")

    if title is None:
        plt.show()
    else:
        plt.savefig(title)


def plotDomains(
    pos_dict: dict, domain_list: list, legend: list, title: str = None
) -> None:
    """
    plots domains for figure legends

    input
    :param pos_dict: site positions on the canvas
    :param domain_list: list of domains
    :param legend: a list containing colors and markers used in the plot [(color, marker), ...]
    :param title: the plot title, if None the plot will not be saved
    """
    fig, ax = plt.subplots(len(domain_list) // 3 + 1, 3, figsize=(10, 6))
    ax = ax.flatten()
    for index, partition in enumerate(domain_list):
        sitesDrawer(
            [pos_dict[i] for i in range(len(pos_dict.keys()))],
            colorDomains(partition),
            {},
            axis=ax[index],
        )
        lineDrawer([pos_dict[i] for i in range(len(pos_dict.keys()))], axis=ax[index])
        ax[index].plot(0.5, 0.4, marker=legend[index][1], color=legend[index][0])

    for axis in ax:
        axis.axis("off")

    if title is None:
        plt.show()
    else:
        plt.savefig(title)


def CombineFigures(
    path_to_graph: str, path_to_legend: str, title: str, rescaler: float = 0
):
    """
    Combines a figure and a legend.

    :param path_to_graph: the path to the graph
    :param path_to_legend: the path to the legend corresponding to the graph
    :param title: name of the new plot
    :param rescaler: allows for manual rescaling of the legend if automatic values do not work out
    """
    graph = Image.open(path_to_graph)
    legend = Image.open(path_to_legend)

    legend = legend.resize((graph.size[0], graph.size[1] + rescaler), Image.ANTIALIAS)

    new_im = Image.new("RGB", (graph.size[0], legend.size[1] + graph.size[1]))

    x_offset = 0
    for im in (graph, legend):
        new_im.paste(im, (0, x_offset))
        x_offset += im.size[1]

    new_im.save(title, dpi=(300, 300))
