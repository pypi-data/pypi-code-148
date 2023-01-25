from typing import List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

import gqcms
from gqcms.Hubbard import Hubbard
from gqcms.matrices.Determinant import Determinant


def format_coefficients(C: np.ndarray, basis: List[Determinant], i: int) -> str:
    """
    Create a string representation with the ith highest probability and the
    corresponding ONV

    :param C: wave function coefficients
    :param basis: ONV basis
    :param i: which ONV to return
    """

    # Compute the probabilities
    probabilities = C**2
    # Sort the coefficients from high to low
    sort_indices = np.argsort(probabilities)[::-1]

    # Return the ith highest coefficients together with its corresponding ONV
    return f"{np.round(probabilities[sort_indices][i], 5)} {np.asarray(basis)[sort_indices][i]} {sort_indices[i]}"


def applyNotebookStyle(fig, x_name, y_name, width, height) -> go.Figure:
    """
    Change width, height and margins of figure and add axis tiltes

    :param fig: plotly figure where the settings will be applied to
    :param x_name: tilte of the x-axis
    :param y_name: tilte of the y-axis
    :param width: width of the figure
    :param height: height of the figure
    """

    # Change marker size and figure size
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=60, r=50, b=70, t=30),
        font=dict(size=30),
        legend=dict(font=dict(size=30))
    )
    fig.update_xaxes(
        title=x_name,
    )
    fig.update_yaxes(
        title=y_name,
    )

    return fig


def applyPaperStyle(fig, x_name, y_name, width=700, height=500, dtick_x=None, dtick_y=None, tickformat_x=None, tickformat_y=None):
    """
    Change width, height, margins and change background color to white.

    :param fig: plotly figure where the settings will be applied to
    :param x_name: tilte of the x-axis
    :param y_name: tilte of the y-axis
    :param width: width of the figure
    :param height: height of the figure
    """

    # Change the marker size
    fig.update_traces(marker=dict(size=4))

    # Change figure width, height, margin and background color
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=60, r=50, b=70, t=30),
        paper_bgcolor="rgba(255, 255, 255, 1)",
        plot_bgcolor="rgba(255, 255, 255, 1)",
        font=dict(size=30),
        legend=dict(font=dict(size=30))        
    )

    # Add x-axis title and change grid line colors and width
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(0,0,0,0.03)",
        title=x_name,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="rgba(0,0,0,0.03)",
        dtick = dtick_x, 
        tickformat = tickformat_x
    )

    # Add y-axis title and change grid line colors and width
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(0,0,0,0.03)",
        title=y_name,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="rgba(0,0,0,0.03)",
        dtick = dtick_y, 
        tickformat = tickformat_y
    )

    return fig


def scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    hubbard: gqcms.Hubbard = None,
    N: int = 4,
    x_name: str = None,
    y_name: str = None,
    dtick_x=None, 
    dtick_y=None, 
    tickformat_x=None, 
    tickformat_y=None,
    height: int = 500,
    width: int = 700,
    style: str = "paper",
    return_fig: bool = False,
    
) -> None:
    """
    Wrapper around plotly.express.scatter that applies some style formating.

    :param df: dataframe or filename to json file where the data is stored
    :param x: column name for the x-axis
    :param y: column name for the y-axis
    :param hubbard: Hubbard object to add ONVs to hover data (default is None)
    :param N: number of highest ONVs to show in hover data (default is 4)
    :param x_name: x-axis name (default is None i.e. the column name of the dataframe)
    :param y_name: y-axis name (default is None i.e. the column name of the dataframe)
    :param height: height of the figure (default is 500)
    :param width: width of the figure (default is 700)
    :param style: style of the figure either notebook or paper (default is notebook)
    :param return_fig: show the figure (False) or return a plotly figure (True) (default is False, i.e show the figure)
    """

    # Load dataframe if a filename is given
    if isinstance(df, str):
        df = pd.read_json(df)

    # Take the N highest ONV coefficients and add to hover data if a Hubbard object is given
    if hubbard is not None:
        for i in range(N):
            df[f"p_m{i}"] = df["C"].apply(
                lambda C: format_coefficients(np.asarray(C), hubbard.basis, i)
            )

        # Create plotly scatter plot
        fig = px.scatter(df, x=x, y=y, hover_data=[f"p_m{i}" for i in range(N)])
    else:
        # Create plotly scatter plot
        fig = px.scatter(df, x=x, y=y)

    # Apply figure settings
    if x_name is None:
        x_name = x
    if y_name is None:
        y_name = y

    if style == "notebook":
        fig = applyNotebookStyle(fig, x_name, y_name, width, height)
    else:
        fig = applyPaperStyle(fig, x_name, y_name, width, height, dtick_x, dtick_y, tickformat_x, tickformat_y)

    # Show figure if 'return_fig' is False, else return the figure
    if not return_fig:
        fig.show()
    else:
        return fig


def scatterPlots(
    df: pd.DataFrame,
    x: str,
    y: str,
    names: List[str] = None,
    hubbard: gqcms.Hubbard = None,
    N: int = 4,
    x_name: str = None,
    y_name: str = None,
    dtick_x=None, 
    dtick_y=None, 
    tickformat_x=None, 
    tickformat_y=None,
    height: int = 500,
    width: int = 700,
    style: str = "paper",
    return_fig: bool = False,
) -> None:
    """
    Wrapper around plotly.express.scatter that applies some style formating.
    Plot multiple traces on one figure from multiple dataframe and one y column
    or one dataframe and multiple y columns

    :param df: dataframe or filename to json file where the data is stored, can be a list if 'y' is a string
    :param x: column name for the x-axis
    :param y: column name for the y-axis, can be a list if one dataframe is given to 'df'
    :param names: name of the traces, if None and y is a list, then the column names are used (default is None)
    :param hubbard: Hubbard object to add ONVs to hover data (default is None)
    :param N: number of highest ONVs to show in hover data (default is 4)
    :param x_name: x-axis name (default is None i.e. the column name of the dataframe)
    :param y_name: y-axis name (default is None i.e. the column name of the dataframe)
    :param height: height of the figure (default is 500)
    :param width: width of the figure (default is 700)
    :param style: style of the figure either notebook or paper (default is notebook)
    :param return_fig: show the figure (False) or return a plotly figure (True) (default is False, i.e show the figure)
    """

    fig = go.Figure()

    # If y is a list of strings and df is of type pd.Dataframe, then plot the all 'y' column names
    # of 'df' on one figure
    if isinstance(y, list) and isinstance(df, pd.DataFrame):
        # Check if names is None, assign y if it is
        if names is None:
            names = y
        
        for i, y in enumerate(y):

            # Take the N highest ONV coefficients and add to hover data
            if hubbard is not None:
                for i in range(N):
                    df[f"p_m{i}"] = df["C"].apply(
                        lambda C: format_coefficients(np.asarray(C), hubbard.basis, i)
                    )

            fig.add_trace(go.Scatter(x=df[x], y=df[y], mode="markers", name=names[i]))

    # If y is a string and df is a list of pd.DataFrame, then plot the given column of all 'df' on
    # figure
    elif isinstance(y, str) and isinstance(df, list):
        for i, dataframe in enumerate(df):
            fig.add_trace(
                go.Scatter(
                    x=dataframe[x], y=dataframe[y], mode="markers", name=names[i]
                )
            )

    # Apply figure settings
    if style == "notebook":
        fig = applyNotebookStyle(fig, x_name, y_name, width, height)
    else:
        fig = applyPaperStyle(fig, x_name, y_name, width, height, dtick_x, dtick_y, tickformat_x, tickformat_y)

    # Show figure if 'return_fig' is False, else return the figure
    if not return_fig:
        fig.show()
    else:
        return fig


def scatterSubPlots(
    df: pd.DataFrame,
    x: str,
    y: str,
    cols: int,
    plot_titles: List[str] = None,
    x_name: str = None,
    y_name: str = None,
    dtick_x=None, 
    dtick_y=None, 
    tickformat_x=None, 
    tickformat_y=None,
    vertical_spacing=None,
    horizontal_spacing=None,
    height: int = 500,
    width: int = 700,
    style: str = "notebook",
    return_fig: bool = False,
) -> None:
    """
    Create subplots using plotly and apply formating

    :param df: dataframe or filename to json file where the data is stored, can be a list if 'y' is a string
    :param x: column name for the x-axis
    :param y: column name for the y-axis, can be a list if one dataframe is given to 'df'
    :param cols: number of columns of the grid where the plots are displayed
    :param hubbard: Hubbard object to add ONVs to hover data (default is None)
    :param N: number of highest ONVs to show in hover data (default is 4)
    :param x_name: x-axis name (default is None i.e. the column name of the dataframe)
    :param y_name: y-axis name (default is None i.e. the column name of the dataframe)
    :param height: height of the figure (default is 500)
    :param width: width of the figure (default is 700)
    :param style: style of the figure either notebook or paper (default is notebook)
    :param return_fig: show the figure (False) or return a plotly figure (True) (default is False, i.e show the figure)
    """

    # The number of rows is determined by the number of given dataframes or y-axis column names
    rows = (
        len(df) // cols + len(df) % cols
        if isinstance(df, list)
        else len(y) // cols + len(y) % cols
    )

    # Add subplot tiltes if they are given
    if plot_titles is not None:
        fig = make_subplots(rows, cols, vertical_spacing=vertical_spacing, horizontal_spacing=horizontal_spacing, subplot_titles=plot_titles)
    else:
        fig = make_subplots(rows, cols, vertical_spacing=vertical_spacing, horizontal_spacing=horizontal_spacing)

    # If y is a string and df is a list of pd.DataFrame, then plot the 'y' column of all dataframes
    # on a seperate plot in the given grid, ploty row and column index starts at one
    if isinstance(y, str) and isinstance(df, list):

        for i, df in enumerate(df):
            fig.add_trace(
                go.Scatter(x=df[x], y=df[y], mode="markers"),
                row=i // cols + 1,
                col=i % cols + 1,
            )

    # If y is a list of strings and df is a pd.Dataframe, then plot all 'y' columns of 'df' on 
    # seperate plots in the given grid, ploty row and column index starts at one
    elif isinstance(y, list) and isinstance(df, pd.DataFrame):
        for i, y_value in enumerate(y):
            fig.add_trace(
                go.Scatter(x=df[x], y=df[y_value], mode="markers"), row=i // cols + 1, col=i % cols + 1
            )

    # Apply figure settings
    if style == "notebook":
        fig = applyNotebookStyle(fig, x_name, y_name, width, height)
    else:
        fig = applyPaperStyle(fig, x_name, y_name, width, height, dtick_x, dtick_y, tickformat_x, tickformat_y)

    # Remove legend
    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=4, color='#636efa'))
    fig.update_annotations(font_size=30)

    # Show figure if 'return_fig' is False, else return the figure
    if not return_fig:
        fig.show()
    else:
        return fig


def plot_all_onv_probabilities(
    result: pd.DataFrame, sys: gqcms.Hubbard, style: str = "paper"
):
    """
    Create a scatter plot showing the probability of each ONV in the system's basis.

    :param result: pandas dataframes where each dataframe must have the columns 'C' and 'expectation_value'
    :param sys: Hubbard system, used for the basis
    :param style: determines the looks of the figure, either 'notebook' or 'paper' (default is 'paper')
    """

    fig = go.Figure()

    # Loop over every ONV in the given basis and plot its probability on the figure
    for i, onv in enumerate(sys.basis):
        fig.add_trace(plot_onv_probability(i, [result], [str(onv)], style).data[0])

    # Apply figure settings
    if style == "notebook":
        fig = applyNotebookStyle(
            fig, x_name="N<sub>os<sub>", y_name="probability", width=700, height=500
        )
    else:
        fig = applyPaperStyle(
            fig, x_name="N<sub>os<sub>", y_name="probability", width=700, height=500
        )

    fig.show()


def plot_onv_probability(
    onv_index: int, results: list, names: list, style: str = "notebook"
):
    """
    Plot the probability of the ONV corresponding with the given index and dataframes in function of the population

    :param onv_index: index of an ONV in the basis list
    :param results: list of pandas dataframes where each dataframe must have the columns 'C' and 'expectation_value'
    :param names: list of trace names
    :param style: determines formatting settings, either 'notebook' or 'paper'
    """
    fig = go.Figure()

    # Compute the probability of the requested ONV and add a trace to the figure
    for i, result in enumerate(results):
        result["p"] = result["C"].apply(lambda C: C[onv_index] ** 2)

        fig.add_trace(
            go.Scatter(
                x=results[i]["expectation_value"],
                y=results[i]["p"],
                mode="markers",
                name=names[i],
            ),
        )

    # Apply figure settings
    if style == "notebook":
        fig = applyNotebookStyle(
            fig, x_name="N<sub>os<sub>", y_name="probability", width=700, height=500
        )
    else:
        fig = applyPaperStyle(
            fig, x_name="N<sub>os<sub>", y_name="probability", width=700, height=500
        )

    return fig


def onv_site_probability(C, state, sites, sys):
    """
    Compute the probability of a given state in a Hubbard system at the given state.
    e.g. compute the probability of an empty state (state = '__') at site zero (sites = 0).
    """

    # Convert sites into list if it is an integer
    if isinstance(sites, int):
        sites = [sites]

    result = 0

    for i, onv in enumerate(sys.basis):
        # Partition the ONV to the given sites
        onv_slice = "\t".join([str(onv)[site * 3 : site * 3 + 2] for site in sites])

        if state in onv_slice:
            result += C[i] ** 2

    return result


def plot_site_probability(df, states, sites, sys, return_fig=True):
    """
    Plot the total probability of the given site states
    """

    ys = []

    for state in states:

        df[f"s{sites}_{state}_probablility"] = df["C"].apply(
            onv_site_probability, state=state, sites=sites, sys=sys
        )

        ys.append(f"s{sites}_{state}_probablility")

    fig = gqcms.scatterPlots(
        df,
        x="expectation_value",
        y=ys,
        x_name="N<sub>os</sub>",
        y_name="probability",
        names=states,
        style="paper",
        return_fig=True,
    )

    if return_fig:
        return fig
    else:
        fig.show()


def imshow(
    image: np.ndarray,
    x: list,
    y: list,
    x_name: str,
    y_name: str,
    color_name: str,
    color_scale: str = "blues",
    dtick_color: float = None,
    dtick_x: float = None,
    dtick_y: float = None,
    tickformat_x: str = None,
    tickformat_y: str = None,
    last_zone: int = None,
    bzones: bool = False,
    bshow: bool = True,
    save_path: str = None,
    bsave: bool = False,
):
    """
    Wrapper around plotly imshow with some settings applied

    :param image: 2d numpy array
    :param x: x axis values, the length must match the second value of the image shape
    :param y: y axis values, the length must match the first value of the image shape
    :param x_name: x axis name
    :param y_name: y axis name
    :param color_name: name of the color axis
    :param color_scale: which color scale to use, must be a plotly color scale string
    :param dtick: difference between two consecutive values on the color bar
    :param last_zone: last zone position (default is Nones)
    :param bzones: add vertical lines to separate the zones between two integer populations (default is False)
    :param bshow: show (True) or return (False) the figure (default is True, i.e show the figure)
    :param save_path: path where the figure will be saved (default is None)
    :param bsave: save the figure or not (default is False)
    """

    fig = px.imshow(
        image,
        aspect="auto",
        x=x,
        y=y,
        color_continuous_scale=color_scale,
        labels=dict(x=x_name, y=y_name, color=color_name),
    )

    if bzones:
        # Raise error if sites is None
        if last_zone is None:
            raise ValueError("Last_zone must be an integer.")

        # Add vertical lines to separate the zones between two integer populations
        for i in range(1, last_zone):
            fig.add_shape(
                type="line",
                xref="x",
                yref="y",
                x0=min(x),
                y0=i,
                x1=max(x),
                y1=i,
                line_color="rgba(0, 0, 0, 0.5)",
            )

    # Apply figure settings
    fig.update_layout(
        autosize=False,
        width=600,
        height=500,
        coloraxis_colorbar=dict(dtick=dtick_color),
        margin=dict(l=60, r=50, b=70, t=30),
        paper_bgcolor="rgba(255, 255, 255, 1)",
        plot_bgcolor="rgba(0, 0, 0, 1)",
        font=dict(size=25),
    )
    fig.update_yaxes(
        autorange=True,
        showgrid=False,
        zeroline=False,
        dtick = dtick_y, 
        tickformat = tickformat_y
    )
    
    # Remve x-axes grid
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        dtick = dtick_x, 
        tickformat = tickformat_x
    )


    # Save figure in static png and interactive html format
    if bsave:
        fig.write_image(f"{save_path}.png")
        fig.write_html(f"{save_path}.html")
    
    # Show the figure if asked, else if not save return the figure
    if bshow:
        fig.show()
    elif not bsave:
        return fig
