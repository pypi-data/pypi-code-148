def ann():
    print('''
import numpy as np



np.random.seed(5)
x = np.random.randn(3,5)
y = (np.random.randn(1,5)>0)
print(x,y),



y




def sig(z):
    s = 1/(1+np.exp(-z))
    return s




def tanh(z):
    s = (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))
    return s




def relu(z):
    s = np.maximum(0,z)
    return s




def l_relu(z):
    s = np.maximum(0.01,z)
    return s





def shape(x,y):
    n_x = x.shape[0]
    n_h1 = 6 #no of nodes layer 1
    n_h2 = 2 #no of nodes layer 2
    n_y=y.shape[0]
    
    return (n_x, n_h1,n_h2 , n_y)





n_x,n_h1,n_h2,n_y = shape(x,y)





def int_parameters(n_x,n_h1,n_h2,n_y):
    np.random.seed(5)
    w1 = np.random.randn(n_h1,n_x)*0.01
    b1 = np.zeros((n_h1,1))
    w2 = np.random.randn(n_h2,n_h1)*0.01
    b2 = np.zeros((n_h2,1))
    w3 = np.random.randn(n_y,n_h2)*0.01
    b3 = np.zeros((n_y,1))
    
    parameters = {"w1":w1,"b1":b1,"w2":w2,"b2":b2,"w3":w3,"b3":b3}
    return parameters





parameters = int_parameters(n_x,n_h1,n_h2,n_y)




def fwd(x,paramaters):
    w1 = parameters["w1"]
    b1 = parameters["b1"]
    w2 = parameters["w2"]
    b2 = parameters["b2"]
    w3 = parameters["w3"]
    b3 = parameters["b3"]
    
    z1 = np.dot(w1,x)+b1
    a1 = relu(z1)
    z2 = np.dot(w2,a1)+b2
    a2 = relu(z2)
    z3 = np.dot(w3,a2)+b3
    a3 = sig(z3)
    
    catch = {"z1":z1,"a1":a1,"z2":z2,"a2":a2,"z3":z3,"a3":a3}
    return a3,catch



a3,catch = fwd(x,parameters)



catch


def cost(a3,y,parameters):
    m = y.shape[1]
    logf = np.multiply(y,np.log(a3))+np.multiply((1-y),np.log(1-a3))
    cost = -np.sum(logf)/m
    return cost



cost(a3,y,parameters)



def reluDerivative(x):
    x[x<=0] = 0
    x[x>0] = 1
    return x



def tanhDerivative(x):
    return (1-x**2)



def lreluDerivative(x):
    x[x<=0] = 0.01
    x[x>0] = 1
    return x



def sigmoidDerivative(x):
    return (x*(1-x))


def bwd(parameters,catch,x,y):
        m = y.shape[1]
        w1 = parameters["w1"]
        b1 = parameters["b1"]
        w2 = parameters["w2"]
        b2 = parameters["b2"]
        w3 = parameters["w3"]
        b3 = parameters["b3"]

        a1 = catch["a1"]
        a2 = catch["a2"]
        a3 = catch["a3"]

        dz3 = a3-y
        dw3 = np.dot(dz3,a2.T)/m
        db3 = np.sum(dz3,axis=1,keepdims=True)/m
        dz2 = np.dot(w3.T,dz3)*reluDerivative(a2)
        dw2 = np.dot(dz2,a1.T)/m
        db2 = np.sum(dz2,axis=1,keepdims=True)/m
        dz1 = np.dot(w2.T,dz2)*reluDerivative(a1)
        dw1 = np.dot(dz1,x.T)/m
        db1 = np.sum(dz1,axis=1,keepdims=True)/m

        grades = {"dw3":dw3,"db3":db3,"dw2":dw2,"db2":db2,"dw1":dw1,"db1":db1}
        return grades


grades = bwd(parameters,catch,x,y)


def update_params(parameters,grades,lr=0.01):
    w1 = parameters["w1"]
    b1 = parameters["b1"]
    w2 = parameters["w2"]
    b2 = parameters["b2"]
    w3 = parameters["w3"]
    b3 = parameters["b3"]

    dw1 = grades["dw1"]
    db1 = grades["db1"]
    dw2 = grades["dw2"]
    db2 = grades["db2"]
    dw3 = grades["dw3"]
    db3 = grades["db3"]

    w1 = w1 - lr*dw1
    b1 = b1 - lr*db1
    w2 = w2 - lr*dw2
    b2 = b2 - lr*db2

    parameters = {"w1":w1,"b1":b1,"w2":w2,"b2":b2,"w3":w3,"b3":b3}

    return parameters

update_params(parameters,grades,lr=0.01)


    ''')


ann()
