
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
    

def hypercube_design(n_factors, target_indx = -2):
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