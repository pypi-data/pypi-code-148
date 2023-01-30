import matplotlib.pyplot as _pyplot

# plot_obj is Figure or Axes or others...


def get_axes(plot_obj=None):
    if isinstance(plot_obj, _pyplot.Axes):
        return plot_obj
    if isinstance(plot_obj, _pyplot.Figure):
        return plot_obj.gca()

    return _pyplot.gca()


def get_figure(plot_obj=None):
    if isinstance(plot_obj, _pyplot.Figure):
        return plot_obj
    if isinstance(plot_obj, _pyplot.Axes):
        return plot_obj.figure

    return _pyplot.gcf()


def set_common_figure_style(plot_obj=None):
    figure = get_figure(plot_obj)

    figure.set_facecolor("#DDDDFF")
    figure.subplots_adjust(
        left=0.05, right=0.95,
        bottom=0.05, top=0.95,
        wspace=0.1, hspace=0.1
    )


def draw_points(x, y, plot_obj=None, **kwargs):
    default_mplrc = {"marker": "x", "alpha": 0.8}
    for key, val in default_mplrc.items():
        if key not in kwargs:
            kwargs[key] = val

    axes = get_axes(plot_obj)
    axes.scatter(x, y, **kwargs)
    return axes


def draw_polygon(poly_xy, plot_obj=None, **kwargs):
    default_mplrc = {
        "closed": True, "fill": False,
        "color": "#3311FF", "alpha": 0.8,
        "linestyle": "dashed", "lw": 3
    }
    for key, val in default_mplrc.items():
        if key not in kwargs:
            kwargs[key] = val

    rect = _pyplot.Polygon(poly_xy, **kwargs)

    axes = get_axes(plot_obj)
    axes.add_patch(rect)
    return axes


def draw_rect(sx, sy, w, h, plot_obj=None, **kwargs):
    return draw_polygon(((sx, sy), (sx+w, sy), (sx+w, sy+h), (sx, sy+h)), plot_obj=plot_obj, **kwargs)


def draw_polygon_opened(poly_xy, plot_obj=None, **kwargs):
    if "closed" not in kwargs:
        kwargs["closed"] = False
    default_mplrc = {
        "closed": False, "fill": False,
        "linestyle": "solid", "lw": 2
    }
    for key, val in default_mplrc.items():
        if key not in kwargs:
            kwargs[key] = val
    return draw_polygon(poly_xy, plot_obj=plot_obj, **kwargs)
