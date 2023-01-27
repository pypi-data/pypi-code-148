def AP(a,d,n):
    for i in range(1,n+1):
        t_n = a + (i-1)*d
        print(t_n)

def APsum(a,d,n):
    S_n = (n/2)*(2*a + (n-1)*d)
    print("Sum of first n terms: ", S_n)

def GP(a,r,n):
    for i in range(1,n+1):
        t_n = a * r**(i-1)
        print(t_n)

def GPsum(a,r,n):
    if(r>1):
        S_n = (a*(r**n))/(r-1)
    else:
        S_n = (a*(r**n))/(1-r)
 
    print("Sum of n terms: ",S_n)

