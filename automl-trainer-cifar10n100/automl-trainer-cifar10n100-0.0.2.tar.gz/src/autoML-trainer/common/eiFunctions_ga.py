import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm, gamma
from .bayesian_optimization_util import plot_approximation, plot_acquisition, plot_convergence
from sklearn.gaussian_process import GaussianProcessRegressor


def expected_improvement(X, X_sample, Y_sample, gpr, xi=0.01):
    ''' Computes the EI at points X based on existing samples X_sample and Y_sample using a Gaussian process surrogate model. 
    Args: X: Points at which EI shall be computed (m x d). 
    X_sample: Sample locations (n x d). 
    Y_sample: Sample values (n x 1). 
    gpr: A GaussianProcessRegressor fitted to samples. 
    xi: Exploitation-exploration trade-off parameter. 
    Returns: Expected improvements at points X. '''
    
    mu, sigma = gpr.predict(X, return_std=True)
#    print("mu: ",mu)
    mu_sample = gpr.predict(X_sample)

    sigma = sigma.reshape(-1, X_sample.shape[1])
    
    # Needed for noise-based model,
    # otherwise use np.max(Y_sample).
    # See also section 2.4 in [...]
    mu_sample_opt = np.max(mu_sample)

#    mu_sample_opt1 = np.min(mu_sample)

    with np.errstate(divide='warn'):
        imp = mu - mu_sample_opt - xi
        Z = imp / (sigma+1e-6)
        ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
        ei[sigma == 0.0] = 0.0
        
#        print("Gau_ei : ", ei)
    return ei

def propose_location(acquisition, X_sample, Y_sample, gpr, bounds, n_restarts=50):
    ''' Proposes the next sampling point by optimizing the acquisition function. Args: acquisition: Acquisition function. X_sample: Sample locations (n x d). Y_sample: Sample values (n x 1). gpr: A GaussianProcessRegressor fitted to samples. Returns: Location of the acquisition function maximum. '''
    dim = X_sample.shape[1]
    min_val = 1
    min_x = None
    
    def min_obj(X):
        # Minimization objective is the negative acquisition function
        return -acquisition(X.reshape(-1, dim), X_sample, Y_sample, gpr)
    
    # Find the best optimum by starting from n_restart different random points.
    for x0 in np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_restarts, dim)):
        res = minimize(min_obj, x0=x0, bounds=bounds, method='L-BFGS-B')
#        print("res.fun[0]: ",res.fun[0], "res.fun: ", res.fun, "res.x: ", res.x.shape)
        if res.fun < min_val:
            min_val = res.fun[0]
            min_x = res.x           
            
    return min_x.reshape(-1, 1)

def expected_improvement_g(X, X_sample, Y_sample, gpr, xi=0.01):
    ''' Computes the EI at points X based on existing samples X_sample and Y_sample using a Gaussian process surrogate model. 
    Args: X: Points at which EI shall be computed (m x d). 
    X_sample: Sample locations (n x d). 
    Y_sample: Sample values (n x 1). 
    gpr: A GaussianProcessRegressor fitted to samples. 
    xi: Exploitation-exploration trade-off parameter. 
    Returns: Expected improvements at points X. '''
    
    mu, sigma = gpr.predict(X, return_std=True)
#    print("mu: ",mu)
    mu_sample = gpr.predict(X_sample)

    sigma = sigma.reshape(-1, X_sample.shape[1])
    
    # Needed for noise-based model,
    # otherwise use np.max(Y_sample).
    # See also section 2.4 in [...]
    mu_sample_opt = np.max(mu_sample)

#    mu_sample_opt1 = np.min(mu_sample)

    with np.errstate(divide='warn'):
        alpha = 0.5
        scale = 0.0093
        imp = mu - mu_sample_opt - xi
        Z = imp / (sigma+1e-6)
        ei = imp * gamma.cdf(Z,alpha) + sigma * gamma.pdf(Z,alpha)
        ei[sigma == 0.0] = 0.0
#        print("gamma ei : ",ei)
        
    return ei

def propose_location_g(acquisition, X_sample, Y_sample, gpr, bounds, n_restarts=50):
    ''' Proposes the next sampling point by optimizing the acquisition function. Args: acquisition: Acquisition function. X_sample: Sample locations (n x d). Y_sample: Sample values (n x 1). gpr: A GaussianProcessRegressor fitted to samples. Returns: Location of the acquisition function maximum. '''
    dim = X_sample.shape[1]
    min_val = 1
    min_x = None
    
    def min_obj(X):
        # Minimization objective is the negative acquisition function
        return -acquisition(X.reshape(-1, dim), X_sample, Y_sample, gpr)
    
    # Find the best optimum by starting from n_restart different random points.
    for x0 in np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_restarts, dim)):
        res = minimize(min_obj, x0=x0, bounds=bounds, method='L-BFGS-B') 
        #print("res : "+str(res))
        if res.fun < min_val:
            min_val = res.fun[0]
            min_x = res.x           
            
    return min_x.reshape(-1, 1)


def plot_approximation(gpr, X, Y, X_sample, Y_sample, X_next=None, show_legend=False):
    mu, std = gpr.predict(X, return_std=True)
    #print("mu :"+str(mu))
    plt.fill_between(X.ravel(), 
                     mu.ravel() + 1.96 * std, 
                     mu.ravel() - 1.96 * std, 
                     alpha=0.1) 
    plt.plot(X, Y, 'y--', lw=1, label='Noise-free objective')
    plt.plot(X, mu, 'b-', lw=1, label='Surrogate function')
    plt.plot(X_sample, Y_sample, 'kx', mew=1, label='Noisy samples')
    plt.plot(X_sample[int(len(X_sample))-1], Y_sample[int(len(Y_sample))-1], 'rx',mew=2,label='New Noisy sample')
    if X_next:
        plt.axvline(x=X_next, ls='--', c='k', lw=1)
    if show_legend:
        plt.legend()

def plot_acquisition(X, Y, X_next, show_legend=False):
#    print("x and Y : ",X," ",Y)
    plt.plot(X, Y, 'r-', lw=1, label='Acquisition function')
    plt.axvline(x=X_next, ls='--', c='k', lw=1, label='Next sampling location')
    if show_legend:
        plt.legend()
def kappa_analysis(val_acc_list, val_loss_list, lam):
    acc_loss = lam*pow(val_acc_list,2) - np.log(val_loss_list/lam)
    for i in acc_loss:
            tmp = np.argmin(acc_loss)
            if acc_loss[tmp] < 0:
                acc_loss[tmp]=0.0 
    return acc_loss
