   
import matplotlib.pyplot as plt
import numpy as np
import scipy 


def parameter_optimization(x_data, y_data, training_fraction = 0.8, normalize_y = True, params = None, training_subset = None, measurement_standard_deviation = 0.0):
    """
    Draft for a parameter optimization scheme
    
    Takes as input the dataset (x_data, y_data) and the 
    fraction (a float in the interval 0.0 - 1.0) of datapoints
    to use as training data.
    """
    n = int(training_fraction*x_data.shape[0])
    
    # special first iteration
    if params is None:
        params = np.ones(x_data.shape[1])*-2.0 #*0.001
    #training_subset = np.random.choice(x_data.shape[0], n, replace = False)
    if training_subset is None:
        training_subset = np.ones(x_data.shape[0], dtype = bool)
        training_subset[n:] = False
    else:
        if len(training_subset)<len(y_data):
            # assume index element array
            ts = np.zeros(len(y_data), dtype = bool)
            ts[training_subset] = True
            training_subset = ts
            
            
    #print(training_subset)
    #print(x_data[training_subset])
        
    #print(training_subset)
    y_data_n = y_data*1
    if normalize_y:
        y_data_n*=y_data_n.max()**-1
        
    
    def residual(params, x_data = x_data, y_data=y_data_n, training_subset = training_subset):
        test_subset = np.ones(x_data.shape[0], dtype = bool)
        test_subset[training_subset] = False
        regressor = Regressor(x_data[training_subset] , y_data[training_subset], measurement_standard_deviation=measurement_standard_deviation) 
        regressor.params = 10**params
        #energy = np.sum((regressor.predict(x_data[test_subset]) - y_data[test_subset])**2)
        energy = np.sum((regressor.predict(x_data) - y_data)**2)
        return energy
    
    
    ret = minimize(residual, params)
    #print(ret)
    return 10**ret["x"]

def parameter_tuner_3d(all_x, all_y, n, measurement_standard_deviation = 0.0, params0 = np.array([1., 1.0, 1.0])):
    """
    Interactive (widget for Jupyter environments) parameter tuner 
    for the gpr module 

    Authors: Audun Skau Hansen and Ayla S. Coder 
    """


    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button



    training_x = all_x[n]
    training_y = all_y[n]
    
    regressor = Regressor(training_x, training_y, measurement_standard_deviation = measurement_standard_deviation, params = params0)


    # The parametrized function to be plotted
    def f(params1, params2, params3):
        regressor.params = 10**np.array([params1, params2, params3])
        return regressor.predict(all_x)



    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots()
    plt.plot(np.arange(len(all_y))[n], all_y[n], "o", markersize = 10, label = "training data", color = (0,0,.5))
    plt.plot(all_y, "o", label = "true values", color = (.9,.2,.4))
    plt.legend()
    line, = plt.plot( f(1,1,1), ".-", lw=1, color = (.9,.9,.2))

    ax.set_xlabel('Time [s]')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(left=0.4, bottom=0.25)
    
    init_values = [1.0, 1.0, 1.0]
    if params0 is not None:
        init_values = [np.log10(i) for i in params0]

    # Make a vertically oriented slider to control the amplitude
    param1 = plt.axes([0.1, 0.3, 0.02, 0.5])
    param_slider1 = Slider(
        ax=param1,
        label="log(P1)",
        valmin=-10,
        valmax=10,
        valinit=init_values[0],
        orientation="vertical"
    )

    # Make a vertically oriented slider to control the amplitude
    param2 = plt.axes([0.2, 0.3, 0.02, 0.5])
    param_slider2 = Slider(
        ax=param2,
        label="log(P2)",
        valmin=-10,
        valmax=10,
        valinit=init_values[1],
        orientation="vertical"
    )

    # Make a vertically oriented slider to control the amplitude
    param3 = plt.axes([0.3, 0.3, 0.02, 0.5])
    param_slider3 = Slider(
        ax=param3,
        label="log(P3)",
        valmin=-10,
        valmax=10,
        valinit=init_values[2],
        orientation="vertical"
    )



    # The function to be called anytime a slider's value changes
    def update(val):
        line.set_ydata( f(param_slider1.val,param_slider2.val,param_slider3.val)) 
        fig.canvas.draw_idle()



    # register the update function with each slider
    #freq_slider.on_changed(update)
    param_slider1.on_changed(update)
    param_slider2.on_changed(update)
    param_slider3.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')


    def reset(event):
        param_slider1.reset()
        param_slider2.reset()
        param_slider3.reset()
    
    button.on_clicked(reset)
    
    
 
    plt.show()

