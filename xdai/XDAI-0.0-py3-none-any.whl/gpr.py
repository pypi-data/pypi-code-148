import numpy as np
from scipy.interpolate import interp1d 
from IPython.display import HTML # for the HTML-table formatting

def central_composite_design(n_factors):
    pts = np.array(np.meshgrid(*[x for i in range(nd)])).reshape(-1,3)
    
    
def hypercube_edge_design(n_factors):
    # Box-Behnken design
    x = np.linspace(-1,1,3)
    xi = range(3)
    pts = np.array(np.meshgrid(*[x for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_indx = np.array(np.meshgrid(*[xi for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_val = np.sum(pts**2, axis = 1)
    target_val = np.sort(np.unique(pts_val))[-2]
    return pts_indx[np.abs(pts_val-target_val)<1e-10]
    
def hypercube_corner_design(n_factors):
    """
    
    """
    x = np.linspace(-1,1,3)
    xi = range(3)
    pts = np.array(np.meshgrid(*[x for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_indx = np.array(np.meshgrid(*[xi for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_val = np.sum(pts**2, axis = 1)
    target_val = np.sort(np.unique(pts_val))[-1]
    return pts_indx[np.abs(pts_val-target_val)<1e-10]


def full_factorial_design(factors):
    if type(factors) is int:
        x = np.linspace(-1,1,3)
        pts = np.array(np.meshgrid(*[x for i in range(nd)])).reshape(-1,3)
    

def hypercube_design(n_factors, target_indx = -1):
    """
    Set up (indexed) factorial design
    
    ## Keyword arguments
    
    | Argument      | Description |
    | ----------- | ----------- |
    |factor_limits   | [[min,max] for each factor] |
    | design | 1 : Corner of hypercube |
    |  | 2 : Mid-/edgepoint design (Box-Behnken) |
    |  | 3 : Face centered design |
    
    ## Returns
    
    A numpy array containing indexes (not values) for the factorial design
    
    """
    # Factorial design patterns
    # target_indx = -1 -- corner, 
    #               -2 -- edges, 
    #               -3 -- faces
    x = np.linspace(-1,1,3)
    xi = range(3)
    pts = np.array(np.meshgrid(*[x for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_indx = np.array(np.meshgrid(*[xi for i in range(n_factors)])).reshape(n_factors,-1).T
    pts_val = np.sum(pts**2, axis = 1)
    target_val = np.sort(np.unique(pts_val))[target_indx]
    return pts_indx[np.abs(pts_val-target_val)<1e-10]


def doe_grid(factor_limits, design = 1, n_center = 3, n_blocks = 1):
    """
    Set up a Design of Experiment grid
    (excluding center points)
    
    ## Keyword arguments
    
    | Argument      | Description |
    | ----------- | ----------- |
    |factor_limits   | [[min,max] for each factor] |
    | design | 1 : Corner of hypercube |
    |  | 2 : Mid-/edgepoint design (Box-Behnken) |
    |  | 3 : Face centered design |
    | n_center | number of points in the center |
    | n_blocks | number of blocks (repetitions) |
    
    ## Returns
    
    A numpy array containing the sample points
    """
    
    indx = hypercube_design(len(factor_limits), -1*design)
    values = interp1d([0,1], np.array(factor_limits))(np.linspace(0,1,3))
    design_shape = np.array(indx.shape)
    design_shape[0] += n_center
    design_pattern = np.zeros(design_shape, dtype = float)
    for i in range(n_center):
        design_pattern[i] = values[:,1]
    for i in range(len(factor_limits)):
        design_pattern[n_center:,i] = values[i][indx[:, i]]     
        
    # repeat blocks
    design_pattern = np.tile(design_pattern.T, n_blocks).T
    
    # insert indexing in first column
    ##annotated_design_pattern = np.zeros(np.array(design_pattern.shape) + np.array([0,1]), dtype = float)
    #annotated_design_pattern[:,0] = np.arange(design_pattern.shape[0])+1
    #annotated_design_pattern[:,1:] = design_pattern
    return design_pattern

def html_table(values, columns = None, rows = None):
    """
    Simple HTML table generator
    """
    ret = """<table>\n"""
    
    nr = values.shape[0]
    nc = values.shape[1]
    
    if columns is not None:
        ret += "<tr>\n"
        #ret += "<th></th>\n"
        
        for c in range(len(columns)):
            ret += "<th>%s</th>\n" % columns[c]
        
        ret += "</tr>\n"
        
    for r in range(nr):
        ret += "<tr>\n"
        if columns is not None:
            if rows is not None:
                ret += "<th>%s</th>\n" % rows[r]
            else:
                ret += "<th></th>\n"
        else:
            if rows is not None:
                ret += "<th>%s</th>\n" % rows[r]
            else:
                ret += "<th></th>\n"

        for c in range(nc):
            ret += "<th>%s</th>\n" % values[r, c]
        ret += "</tr>\n"
    ret += """</table>\n"""
    
    return HTML(ret)



## 




from scipy.stats import multivariate_normal, norm
import numpy as np

import numpy as np
#from btjenesten import kernels as knls
#import btjenesten.kernels as knls
#from btjenesten.kernels import RBF
#import kernels as knls
from scipy.optimize import minimize, LinearConstraint

def RBF(X1, X2, l = np.array([1.0])):
    """
    Radial basis function of the form:
    $$
    e^{-l * d(X_i,X_j)}
    $$
    Parameters:
    -----------
    X1: Dataset 1
    
    X2: Dataset 2
    l: Length scale parameter. 
    Can be adjusted to adjust the covariance between $x_i$ and $x_j$. 
    Increasing l will decrease the covariance, and vice versa.
    
    Returns:
    -----------
    A matrix with the same shape as our input data, where the elemets are:
    $e^{-l \cdot d(x_i, x_j)}$ where $d(x_i, x_j)$ is the difference between element $x_i$ in X1
    and element $x_j$ in X2.
    """
    
    if type(l) is not np.ndarray:
        # patch for scalar length parameter
        l = np.array([l])

    ld = np.sum(l[None, :]*(X1.reshape(X1.shape[0],-1)[:, None] - X2.reshape(X2.shape[0],-1)[None,])**2, axis = 2)

    return np.exp(-ld)

class Kernel():
    """
    Kernel class 
    Parameters:
    -----------
    covariance_function:
    The function that will be used to calculate the covariance between our datasets
    """

    def __init__(self, covariance_function):
        self.covariance_function = covariance_function
        
    
    def K(self, X1, X2, params):
        """
        Function that returns the covariance matrix given our datasets
        Parameters:
        -----------
        X1: Dataset 1 (Often the training set)
        X2: Dataset 2 (Often the target set)
        Returns:
        ----------
        self.covariance_function(X1, X2) : covariance matrix given our datasets X1 and X2.
        """
        
        if np.isscalar(X1):
            X1 = np.array([X1])
        if np.isscalar(X2):
            X2 = np.array([X2])

        return self.covariance_function(X1, X2, params) 


class Regressor():
    """
    Gaussian process regressor class
    Parameters:
    -----------
    kernel:
    Specifies the type of covarince function we want for our regressor. 
    If none is provided the default is the radial basis function
    training_data_X: 
    Training data inputs, also called features
    training_data_Y:
    Training data outputs, also called labels
    params:
    
    """

    def __init__(self, training_data_X, training_data_Y, kernel = None, params = 1, measurement_standard_deviation = 0):
        if kernel == None:
            self.kernel = Kernel(RBF)
        else:
            self.kernel = Kernel(kernel)
            
        self.measurement_standard_deviation = measurement_standard_deviation
            
            

        msg = "Expected 2D array. If you only have one feature reshape training data using array.reshape(-1, 1)"
        assert training_data_X.ndim != 1, msg
        
        
        self.training_data_X = training_data_X
        self.training_data_Y = training_data_Y

        self.params = params # 
        
        self.acquisition_function = self.acquisition_UCB

    def predict(self, input_data_X, training_data_X = None, training_data_Y = None, return_variance = False):
        """
        Predicts output values for some input data given a set of training data 
        Parameters:
        -----------
        input_data_X:
        Input features that the gpr will evaluate.
        training_data_X:
        training data inputs.
        training_data_Y:
        training data outputs.
        
        return_variance:
        Returns variance for each prediction if this is true
        Returns:
        -----------
        predicted_y:
        Predicted output data given cooresponding input_data_X and a set of training data
        inputs and outputs (training_data_X, training_data_Y)
        
        predicted_variance:
        Predicted variance for each point of predicted output.
        """

        if training_data_X == None or training_data_Y == None:
            K_11 = self.kernel.K(self.training_data_X, self.training_data_X, self.params)
            
            # white noise kernel (only if measurement_standard_deviation != 0)
            K_11 += np.eye(self.training_data_Y.shape[0])*self.measurement_standard_deviation
            
            K_12 = self.kernel.K(self.training_data_X, input_data_X, self.params)
            K_21 = K_12.T
            K_22 = self.kernel.K(input_data_X, input_data_X, self.params)
            K_22 += np.eye(input_data_X.shape[0])*self.measurement_standard_deviation
            
            
            assert (np.linalg.det(K_11) != 0), "Singular matrix. Training data might have duplicates."
            
            KT = np.linalg.solve(K_11, K_12).T
            
            
            predicted_y = KT.dot(self.training_data_Y)
            
        else:
            K_11 = self.kernel.K(training_data_X, training_data_X, self.params)
            # white noise kernel (only if measurement_standard_deviation != 0)
            K_11 += np.eye(self.training_data_Y.shape[0])*self.measurement_standard_deviation
            
            K_12 = self.kernel.K(training_data_X,input_data_X, self.params)
            K_21 = self.kernel.K(input_data_X, training_data_X, self.params)
            K_22 = self.kernel.K(input_data_X, input_data_X, self.params)
            K_22 += np.eye(input_data_X.shape[0])*self.measurement_standard_deviation
            
            assert (np.linalg.det(K_11) != 0), "Singular matrix. Training data might have duplicates."
            KT = np.linalg.solve(K_11, K_12).T

            predicted_y = KT.dot(training_data_Y)

        predicted_y = predicted_y.ravel()

        if return_variance:
            predicted_variance = np.diag(K_22 - KT @ K_12)
            
            y_var_negative = predicted_variance < 0
            if np.any(y_var_negative):
                predicted_variance.setflags(write="True")
                predicted_variance[y_var_negative] = 0

            return predicted_y, predicted_variance
        else:
            return predicted_y

    def score(self, input_data_X, input_data_Y):
        """
        Returns the average and maximum error of our predict method.
        Parameters:
        -----------
        input_data_X:
        input data that the gpr will predict corresponding output data to.
        input_data_Y:
        Corresponding true ouput data for input_data_X.
        Returns:
        --------
        avg_error - the average error between the predicted values and the true values
        max_error - the maximum error between the predicted values and the true values
        """

        predicted_y = self.predict(input_data_X)
        avg_error = np.mean(np.abs(predicted_y - input_data_Y))
        max_error = np.max(np.abs(predicted_y - input_data_Y))
        return avg_error, max_error
        
    def predict_sample_optimum(self, initial_guess, bounds = None, maximize = False, xi = 0.01, tol = 1e-8):
        """
        Predict a optimal point for new measurements
        """
        
        # selector for minimization/maximization 
        prefactor = 1.0
        if maximize:
            prefactor = -1.0
        
        # define objective function / acquisition function to minimize/maximize
        def objective(x, f = self.acquisition_function):
            x = x.reshape(1, -1)
            return prefactor*f(x, xi)
        

        # set contraints / bounds for optimization
        if bounds is None:
            constraints = ()
            
        else:
            lower_bounds = bounds[0]
            upper_bounds = bounds[1]
            A = np.eye(len(initial_guess))
            #print("constraint shape:", A.shape, lower_bounds.shape, upper_bounds.shape)
            constraints = LinearConstraint(A, lb=lower_bounds, ub=upper_bounds) #, keep_feasible=False)
            
        # perform optimization
        minimization = minimize(objective, initial_guess, constraints = constraints, tol = tol, method = "COBYLA", options = {"maxiter":10000})
        #minimization = minimize(objective, initial_guess, constraints = constraints,method = "COBYLA")
        #minimization = minimize(objective, initial_guess) #, constraints = constraints, tol = 1e-15, method = "COBYLA")
        
        # return results
        #print(minimization)
        if minimization.success:
            return minimization.x, minimization.fun, minimization.success
        else:
            return minimization.x, minimization.fun, minimization.success
        
        
    def acquisition_function(self, x):
        """
        placeholder function
        """
        pass

    
    
    def acquisition_EI(self, x, xi = 0.01):
        """
        Returns the expected improvement of our model at some given x, in comparison to the current best measurement.
        
        Parameters:
        -----------
        x: The position where the expected improvement will be calculated.
        
        xi: Exploration parameter. An increase in xi will give an increase in exploration.
        
        Returns:
        --------
        EI:
        The expected improvement in x.
        """
        mu, variance = self.predict(x, return_variance = True)
        EI = np.zeros(len(mu), dtype = float) # if variance is zero, well return 0
        
        #EI[] = 
        
        ci = variance>1e-14


        sigma = variance**.5

        f_best = np.min(self.training_data_Y) #this line may be wrong (upon minimization)

        z = mu - f_best - xi
        Z = np.zeros(len(mu), dtype = float)

        Z[ci] = z[ci]/sigma[ci]

        EI[ci] = norm().cdf(Z[ci])*z[ci] + norm().pdf(Z[ci])*sigma[ci]
      
        return EI
    
    def acquisition_UCB(self, x, xi = 0.01):
        """
        Returns the expected improvement of our model at some given x, in comparison to the current best measurement.
        
        Parameters:
        -----------
        x: The position where the expected improvement will be calculated.
        
        xi: Exploration parameter. An increase in xi will give an increase in exploration.
        
        Returns:
        --------
        EI:
        The expected improvement in x.
        """
        mu, variance = self.predict(x, return_variance = True)
        sigma = variance**.5
        
        return mu - xi*sigma
        

    def acquisition_UCB_(self, minimize_prediction=True, x0 = None, l=1.2, delta=0.1, method = "COBYLA"):
        """
        Returns the point at which our model function is predicted to have the highest value.
        Parameters:
        -----------
        minimize_prediction:
        If your task is to minimize some model function, this parameter is True. If your task is to maximize the model function
        this parameter is False.
        alpha:
        Exploration parameter. Scales how much the standard deviation should impact the function value. alpha = 1.2
        means that the function maximized/minimized equals predicted value +/- the standard deviation.
        
        x0:
        Initial guess. If not specified it will use the point at which the training data is the largest/smallest.
        delta:
        Hyperparameter that tunes UCB around measured datapoints.
        
        Returns:
        --------
        p - The predicted point at which an evaluation would yield the highest/lowest value
        """
        if minimize_prediction: #Minimization process
            if x0 == None:
                x0_index = np.where(self.training_data_Y == np.min(self.training_data_Y))

                x0 = self.training_data_X[x0_index]

            objective_function = lambda x, predict = self.predict : predict(x)
            std_x = lambda x, predict = self.predict : np.sqrt(np.abs(np.diag(predict(x, return_variance = True)[1])))
            objective_noise = lambda x, std = std_x : (1 - std(x))**2 * delta + std(x)

            UCB = lambda x, exploit = objective_function, explore = objective_noise: exploit(x) + alpha*explore(x) 

            def UCB(x, f = self.acquisition_EI):
                x = x.reshape(1, -1)
                return f(x)

            minimization = minimize(UCB, x0, method = method)
            p = minimization.x
            return p

        else: #Maximization process
            if x0 == None:
                x0_index = np.where(self.training_data_Y == np.max(self.training_data_Y))

                x0 = self.training_data_X[x0_index]

            objective_function = lambda x, predict = self.predict : predict(x)
            std_x = lambda x, predict = self.predict : np.sqrt(np.abs(np.diag(predict(x, return_variance = True)[1])))
            objective_noise = lambda x, std = std_x : (1 - std(x))**2 * delta + std(x)

            UCB = lambda x, exploit = objective_function, explore = objective_noise : -1*(exploit(x) + alpha*explore(x))
            def UCB(x, f = UCB):
                x = x.reshape(1, -1)
                return f(x)

            minimization = minimize(UCB, x0, method = method)
            p = minimization.x
            return p
        

    def update(self, new_X, new_Y, tol=1e-5):
        """
        Updates the training data in accordance to some newly measured data.
        Parameters:
        -----------
        new_X:
        Set of new features that have been measured.
        new_Y:
        Corresponding set of labels to new_X.
        tol:
        Tolerance which the training data set can differ from new points. If this is too low you may encounter singular 
        covariance matrices.
        """

        assert type(new_Y) is np.ndarray, "Data error!!!!! Needs to be array."
        assert type(new_X) is np.ndarray, "Data error!!!!! Needs to be array."

        for measurement in new_X.reshape(-1, self.training_data_X.shape[1]):
            for i in range(len(self.training_data_X)):
                if np.allclose(measurement, self.training_data_X[i], atol = tol):
                    print(f"The model has most likely converged! {measurement} already exists in the training set.")
                    return True
        """
        old_X_shape = self.training_data_X.shape
        old_Y_shape = len(self.training_data_Y)
        new_X_shape = np.array(self.training_data_X.shape)
        new_Y_shape = len(new_Y)
        new_X_shape[0] += new_X.shape[0]
        new_Y_shape += len(new_Y)
        new_training_data_X = np.zeros(new_X_shape)
        new_training_data_Y = np.zeros(new_Y_shape)
        new_training_data_X[:-old_X_shape.shape[0]] = self.training_data_X
        new_training_data_X[-new_X.shape[0]:] = new_X 
        new_training_data_Y[:-old_Y_shape] = self.training_data_Y
        new_training_data_Y[-new_Y_shape:] = new_Y
        """
        #print("X1 shape ",self.training_data_X.shape)
        #print("X2 shape ",.shape)
        new_X = new_X.reshape(-1, self.training_data_X.shape[1])

        new_training_data_X = np.concatenate((self.training_data_X, new_X))
        new_training_data_Y = np.concatenate((self.training_data_Y, new_Y))

        #indexes = np.argsort(new_training_data_X)

        self.training_data_X = new_training_data_X#[indexes]
        self.training_data_Y = new_training_data_Y#[indexes]
        
        
        return False

def normalize_training_data_x(training_data):
    """
    generate functions to normalize and recover unnormalized
    training data
    
    
    (more detailed explanation is required)
    """
    mean  = np.mean(training_data, axis =0 )
    bound = np.max(training_data, axis = 0)-np.min(training_data, axis = 0)
    
    def normalize(training_data, mean= mean, bound = bound):
        training_data_normalized = training_data - mean[None,:]
        training_data_normalized *= (.5*bound[None, :])**-1
        return training_data_normalized
    
    def recover(training_data_normalized, mean= mean, bound = bound):
        return training_data_normalized*(.5*bound[None,:]) + mean[None, :]
        
    return normalize, recover

def normalize_training_data_x_log(training_data):
    """
    generate functions to normalize and recover unnormalized
    training data
    
    
    (more detailed explanation is required)
    """
    #mean  = np.mean(training_data, axis =0 )
    min_ = np.min(training_data, axis =0 )  - 1e-3
    bound = np.max(training_data, axis = 0)-np.min(training_data, axis = 0)


    
    def normalize(training_data, min_= min_, bound = bound):
        training_data_normalized = training_data 

        return np.log(training_data_normalized)
    
    def recover(training_data_normalized, min_= min_, bound = bound):
        return np.exp(training_data_normalized)
        
    return normalize, recover

def no_normalization(training_data):
    """
    generate functions which essentially does nothing
    
    """
    def normalize(training_data):
        return training_data
    
    def recover(training_data):
        return training_data
        
    return normalize, recover

def remove_redundancy(x_train, y_train, tol = 10e-8):
    """
    extract unique columns of x_train (and corresponding elements in y_train)
    
    """


    ns = x_train.shape[0] #number of measurements

    # compute the "euclidean distance"
    d = np.sum((x_train[:, None] - x_train[None, :])**2, axis = 2)


    
    active = np.ones(ns, dtype = bool)
    
    
    unique_training_x = []
    unique_training_y = []

    for i in range(ns):

        distances = d[i]
        
        da = distances[active]
        ia = np.arange(ns)[active]
        
        elms = ia[da<tol]
        active[elms] = False
        
        if len(elms)>0:
            unique_training_x.append(x_train[elms[0]])
            unique_training_y.append(np.mean(y_train[elms], axis = 0))


    return np.array(unique_training_x), np.array(unique_training_y)
    
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

