import matplotlib.ticker as ticker
import numpy as np

def plot_convergence(
        figure, convergence, epsilon,
        col_0="C0", col_1="C1"):
    """
    Creates a convergence plot.

    Paramters
    ---------
    figure : Figure
        The matplotlib Figure, which holds all plot elements.
    convergence : list
        The convergence data for each frame.
    epsilon : float
        The tolerance value.
    col_0 : str, optional
        The color code used for the tolerance data scatter points.
        Default = "C0".
    col_1 : str, optional
        The color code used for the tolerance data line.
        Default = "C1".

    """

    # Create axis
    ax = figure.add_subplot()
    
    # Segments start
    ax.axvline(x=-0.5, color="k", linestyle=":", linewidth=1)

    # Plot convergence progress starting with the first iteration
    iter_start = 0
    for conv_frame in convergence:
        # Retrieve the elements with the maximum error 
        # for each frame in the convergence data 
        conv_data = list(max(conv_iter)[0] for conv_iter in conv_frame)
        num_elements = len(conv_data)
        iter_data = np.linspace(
            iter_start, iter_start + num_elements - 1, num_elements)

        # Plot markers for the retrieved values
        ax.scatter(
            iter_data, conv_data, color=col_1, marker="o", alpha=0.4)

        # Now plot a line and mark only the first and the last element
        markevery = (0, max(len(conv_frame) - 1, 1))
       
        ax.plot(
            iter_data, conv_data, color=col_0, marker="o",
            linestyle="-", markevery=markevery,
            label="$\\varphi(y_i)$" if iter_start == 0 else None)

        # Set the new iteration start value
        iter_start += num_elements

    # Plot the segment limits again starting with the first iteration
    iter_start = 0
    for conv_frame in convergence:
        conv_data = list(max(conv_iter)[0] for conv_iter in conv_frame)
        num_elements = len(conv_data)
        iter_start += num_elements
        
        # Draw a vertical line
        ax.axvline(
            x=iter_start - 0.5, color="k", 
            linestyle=":", linewidth=1, alpha=1)

    # Plot the tolerance value epsilon as a red horizontal line
    ax.plot(
        [0, iter_start], [epsilon, epsilon],
        color="r", linestyle="-", linewidth=1,
        label="$\epsilon={}$".format(epsilon))
    ax.axhline(y=epsilon, color="r", linestyle="-", linewidth=1)

    # Set y-axis to logarithmic scale
    ax.set_yscale("log")

    # Set axis labels
    ax.set_xlabel("Iteration [-]")
    ax.set_ylabel("$\\varphi(y_i)$ [-]")
    
    # Enable grid
    ax.grid(which="major", axis="y")
    if len(convergence) > 0:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    else:
        ax.xaxis.set_major_locator(ticker.FixedLocator([0]))
        ax.set_xticklabels([""])

    # Add the legend
    ax.legend(loc=1)

def plot_iterations(
        figure, statistics, epsilon, 
        col_0="C0", col_1="C1", col_2="C3"):
    """
    Creates an iterations plot.

    Paramters
    ---------
    figure : Figure
        The matplotlib Figure, which holds all plot elements.
    statistics : list
        The iteraton results for each frame.
    epsilon : float
        The tolerance value.
    col_0 : str, optional
        The color code used for finished frames.
        Default = "C0".
    col_1 : str, optional
        The color code used for restarted frames.
        Default = "C1.
    col_2 : str, optional
        The color code used for canceled frames.
        Default = "C3".

    """

    # Create axis
    ax = figure.add_subplot()

    # Create data lists
    num_frame = [row[1] for row in statistics]
    error = [row[7] for row in statistics]

    # Retrieve the finished, reastarted an canceled frames from the data
    num_frame_finished = [row[1] for row in statistics if row[2] == "Finished"]
    num_iter_frame_finished = [row[6] for row in statistics if row[2] == "Finished"]

    num_frame_restarted = [row[1] for row in statistics if row[2] == "Restarted"]
    num_iter_frame_restarted = [row[6] for row in statistics if row[2] == "Restarted"]

    num_frame_canceled = [row[1] for row in statistics if row[2] == "Canceled"]
    num_iter_frame_canceled = [row[6] for row in statistics if row[2] == "Canceled"]

    # Plot the restarted frames
    if len(num_frame_restarted):
        ax.bar(
            num_frame_restarted, num_iter_frame_restarted, 
            color=col_1, alpha=0.4, label="Restarted")
       
    # Plot the finished frames
    ax.bar(
        num_frame_finished, num_iter_frame_finished, 
        color=col_0, alpha=0.4, label="Finished")
    
    # Plot the canceled frames
    if len(num_frame_canceled):
        ax.bar(
            num_frame_canceled, num_iter_frame_canceled, 
            color=col_2, alpha=0.4, label="Canceled")

    # Set axis labels
    ax.set_ylabel("Iterations [-]")
    ax.set_xlabel("Frames [-]")

    # Set axismajor locators
    if len(statistics) > 0:
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    else:
        ax.xaxis.set_major_locator(ticker.FixedLocator([0]))
        ax.set_xticklabels([""])

    # Enable grid
    ax.grid(axis="y")

    # Twin axis
    ax2 = ax.twinx() 

    # Plot the convergence results
    ax2.plot(
        num_frame, error, color=col_0, 
        linestyle="-", marker="o",
        label="$\\varphi(y_i)$")

    # Set axis labels and style
    if np.any(error):
        ax2.set_yscale("log")
    ax2.set_ylabel("$\\varphi(y_i)$ [-]")

    # Plot the tolerance value epsilon as a red horizontal line
    ax2.axhline(y=epsilon, color="r", linestyle="-", linewidth=1.0)
    ax2.plot(
        num_frame, np.full(len(num_frame), epsilon), 
        color="r", linestyle="-", linewidth=1.0, 
        label="$\epsilon={}$".format(epsilon))
    
    # Get handles and labels
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Add legend
    ax2.legend(handles1+handles2, labels1+labels2, loc=1)