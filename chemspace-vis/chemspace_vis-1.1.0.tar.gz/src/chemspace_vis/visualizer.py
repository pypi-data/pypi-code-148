

def make_visualizer_script(tsne_filename, img_folder, activity_filename=None, use_log10=True):
    script_str = """import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import random


def interactive_plot(x, y, c, img_list, use_log10=True):
    # Modified from this: https://stackoverflow.com/questions/42867400/python-show-image-upon-hovering-over-a-point
    if use_log10:
        c = np.log10(c)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Embedding 1")
    ax.set_ylabel("Embedding 2")
    line = plt.scatter(x, y, c=c, s=20, cmap="viridis")
    image = plt.imread(img_list[0])
    im = OffsetImage(image, zoom=0.5)
    xybox = (150., 150.)
    ab = AnnotationBbox(im, (0, 0), xybox=xybox, xycoords='data', boxcoords="offset points", pad=0.3,
                        arrowprops=dict(arrowstyle="->"))
    ax.add_artist(ab)
    ab.set_visible(False)

    def hover(event):
        if line.contains(event)[0]:
            indices = line.contains(event)[1]["ind"]
            if len(indices) > 1:
                ind = random.choice(indices)
            else:
                ind = indices[0]
            w, h = fig.get_size_inches() * fig.dpi
            ws = (event.x > w / 2.) * -1 + (event.x <= w / 2.)
            hs = (event.y > h / 2.) * -1 + (event.y <= h / 2.)
            ab.xybox = (xybox[0] * ws, xybox[1] * hs)
            ab.set_visible(True)
            ab.xy = (x[ind], y[ind])
            im.set_data(plt.imread(img_list[ind]))
        else:
            ab.set_visible(False)
        fig.canvas.draw_idle()
    fig.canvas.mpl_connect('motion_notify_event', hover)
    fig = plt.gcf()
    fig.set_size_inches(12, 8)
    plt.show()


def run_interact_plot(tsne_filename, img_folder, activity_filename=None, use_log10=True):
    if img_folder.endswith('/'):
        img_folder = img_folder[:-1]
    with open(tsne_filename) as f:
        lines = f.readlines()
    x = np.zeros(len(lines)-1)
    y = np.zeros(len(lines)-1)
    img_list = []
    for i, line in enumerate(lines[1:]):
        ll = line.split()
        img_list.append('{}/{}.png'.format(img_folder, ll[0]))
        x[i] = float(ll[1])
        y[i] = float(ll[2])
    c = np.zeros(len(x))
    if activity_filename is not None:
        with open(activity_filename) as f:
            lines = f.readlines()
        for i, line in enumerate(lines[1:]):
            c[i] = float(line.split()[-1])
    interactive_plot(x, y, c, img_list, use_log10=use_log10)


if __name__ == "__main__":
    run_interact_plot(""" + """'{}', '{}'""".format(tsne_filename, img_folder)
    if activity_filename is not None:
        script_str += ", activity_filename='{}'".format(activity_filename)
    if use_log10:
        script_str += ", use_log10=True)\n"
    else:
        script_str += ", use_log10=False)\n"
    with open("visualizer_script.py", "w") as f:
        f.write(script_str)

