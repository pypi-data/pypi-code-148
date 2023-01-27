def linear_logistic():
    print('''
import numpy as np

def customlinear(x,y,epoch=50):

    y=y.reshape(-1,1)#convert y into 2d matrix
    m=y.shape[0]# no of training examples
    lr=.01
    nx=x.shape[1]#no of features
    w=np.random.rand(nx+1,1)# weights matrix theta values
    x=np.concatenate((np.ones((m,1)),x),axis=1)# adds a column of 1s in our x


    for i in range(epoch):
        h= np.dot(x,w) #y
        error=h-y
        cost=np.dot(error.T,error)/(2*m) # sum(error**2)/(2*m)


        dw=np.dot(x.T,error)/m
        # print(dw)
        w = w - lr*dw
    return w
   
def sigmoid(z):
    s=1/(1+np.exp(-z))
    # pred=np.where(s>0.5,1,0)
    return s

   
def customlogistic(x,y,epoch=1000):
    y=y.reshape(-1,1)
    m=y.shape[0]
    lr=.01
    nx=x.shape[1]
    w=np.random.rand(nx+1,1)
    x=np.concatenate((np.ones((m,1)),x),axis=1)
    for i in range(epoch):
        h=sigmoid(np.dot(x,w))


        logp= - (np.multiply(y,np.log(h))   +   np.multiply((1-y),np.log(1-h)))
        cost= np.sum(logp)/m

        if i%100==0:
            print(h)
            print(f"Cost: {cost} ==> epoch: {i}")

        error=h-y
        dw = np.dot(x.T,error)/m
        w = w - lr*dw
   

    return w

x = np.array([[1,3], [6,4], [7,6], [9,8]])
y = np.array([1, 0, 0, 1])
print(y.shape)

customlogistic(x,y)

X1=np.array([5,7,8,7,2,17,2,9,4,11,12,9,6]).reshape(-1,1)
X2=np.array([10,14,16,14,4,34,4,18,8,22,24,18,12]).reshape(-1,1)
# len(X1), len(X2)
Y=np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])

X=np.concatenate((X1, X2), axis=1)
X

customlinear(X, Y)



''')


linear_logistic()
