from re import L
import matplotlib as mpl


# temp
import bluebelt
import plotly.graph_objects as go


def linestyle(value):

    # matplotlib "solid", "dotted", "dashed", "dashdot"
    # plotly "solid", "dot", "dash", "dashdot"

    values = {"solid": "solid", "dotted": "dot", "dashed": "dash", "dashdot": "dashdot"}

    if value in values.keys():
        return values.get(value)
    else:
        return None

def marker(value):
    values = {
        "o": "circle",
        "v": "triangle-down",
        "^": "triangle-up",
        "<": "triangle-left",
        ">": "triangle-right",
        "+": "cross",
        "1": "y-down",
        "2": "y-up",
        "3": "y-left",
        "4": "y-right",
        "s": "square",
        "p": "pentagon",
        "8": "octagon",
        "*": "star",
        "x": "x",
        "D": "diamond",
        "d": "diamond-tall",
        }

    return values.get(value, "circle")
    
def tick_direction(value):
    return {"in": "inside", "out": "outside", "inout": "outside"}.get(value)


def get_margin(title=None):
    return dict(
        l=0,
        r=0,
        t=30 if title else 0,
        b=0,
    )


def xaxis(xlabel=None, xlim=None, format_xticks=None):
    return dict(
        title=xlabel,
        gridcolor=mpl.colors.to_hex(mpl.rcParams["grid.color"])
        if mpl.rcParams["axes.grid.axis"] in ["x", "both"]
        else None,
        gridwidth=mpl.rcParams["grid.linewidth"]
        if mpl.rcParams["axes.grid.axis"] in ["x", "both"]
        else None,
        showgrid=True
        if mpl.rcParams["axes.grid.which"] in ["major", "both"]
        else False,
        ticks=tick_direction(mpl.rcParams["xtick.direction"])
        if mpl.rcParams["axes.spines.bottom"]
        else "",
        tickwidth=mpl.rcParams["xtick.major.width"],
        tickcolor=mpl.colors.to_hex(mpl.rcParams["xtick.color"]),
        ticklen=mpl.rcParams["xtick.major.size"],
        tickformat=format_xticks,
        showline=mpl.rcParams["axes.spines.bottom"],
        linecolor=mpl.colors.to_hex(mpl.rcParams["axes.edgecolor"]),
        linewidth=mpl.rcParams["axes.linewidth"],
        mirror=mpl.rcParams["xtick.major.top"],
        range=xlim,
    )


def yaxis(ylabel=None, ylim=None, format_yticks=None):
    return dict(
        title=ylabel,
        gridcolor=mpl.colors.to_hex(mpl.rcParams["grid.color"])
        if mpl.rcParams["axes.grid.axis"] in ["y", "both"]
        else None,
        gridwidth=mpl.rcParams["grid.linewidth"]
        if mpl.rcParams["axes.grid.axis"] in ["y", "both"]
        else None,
        showgrid=True
        if mpl.rcParams["axes.grid.which"] in ["major", "both"]
        else False,
        ticks=tick_direction(mpl.rcParams["ytick.direction"])
        if mpl.rcParams["axes.spines.left"]
        else "",
        tickwidth=mpl.rcParams["ytick.major.width"],
        tickcolor=mpl.colors.to_hex(mpl.rcParams["ytick.color"]),
        ticklen=mpl.rcParams["ytick.major.size"],
        tickformat=format_yticks,
        showline=mpl.rcParams["axes.spines.left"],
        linecolor=mpl.colors.to_hex(mpl.rcParams["axes.edgecolor"]),
        linewidth=mpl.rcParams["axes.linewidth"],
        mirror=mpl.rcParams["ytick.major.right"],
        range=ylim,
    )


def layout(
    title=None,
    xlabel=None,
    ylabel=None,
    xlim=None,
    ylim=None,
    format_xticks=None,
    format_yticks=None,
    legend=True,
    **kwargs,
):

    layout = dict(
        title=title,
        plot_bgcolor=mpl.rcParams["figure.facecolor"],
        hovermode="closest",
        margin=get_margin(title=title),
        xaxis=xaxis(xlabel=xlabel, xlim=xlim, format_xticks=format_xticks),
        yaxis=yaxis(ylabel=ylabel, ylim=ylim, format_yticks=format_yticks),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        showlegend=legend,
    )
    if not kwargs.get('dash', False):
        layout['width']=mpl.rcParams["figure.figsize"][0] * mpl.rcParams["figure.dpi"]
        layout['height']=mpl.rcParams["figure.figsize"][1] * mpl.rcParams["figure.dpi"]
    else:
        layout['paper_bgcolor']='rgba(0,0,0,0)'
        layout['plot_bgcolor']='rgba(0,0,0,0)'
        layout['legend'] = dict(bgcolor='rgba(0,0,0,0)', yanchor="top", xanchor="right")

    return layout

def to_rgba(hex, alpha):
    return 'rgba' + str(mpl.colors.to_rgba(hex +  format(int(255*alpha), 'x')))


def _default_plotly():
    if bluebelt.config('plotting') == 'matplotlib':
        pass
    elif bluebelt.config('plotting') == 'plotly':

        layout = go.Layout(
                m2p.layout(
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    xlim=xlim,
                    format_xticks=format_xticks,
                    legend=legend,
                    **kwargs,
                )
            )

        line_width = np.maximum(1, bluebelt.style("equal_means.boxplot.boxes.linewidth"))
        
        data = [
            go.Box(
                x=plot_obj.frame[col],
                y0=idx,
                marker=dict(color=bluebelt.style("equal_means.boxplot.fliers.color"), symbol=m2p.marker(bluebelt.style("equal_means.boxplot.fliers.marker"))),
                fillcolor=bluebelt.style("equal_means.boxplot.boxes.facecolor"),
                line_color=bluebelt.style("equal_means.boxplot.boxes.edgecolor"),
                line_width=line_width,
                hoverinfo='skip',
                showlegend=False,
                name=col,
            ) for idx, col in enumerate(plot_obj.frame.columns[::-1])
        ]

        fig = go.Figure(data=data, layout=layout)

        return fig
    
    else:
        return