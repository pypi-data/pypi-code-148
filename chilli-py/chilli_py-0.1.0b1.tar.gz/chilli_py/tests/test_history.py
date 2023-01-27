from chilli_py.utils import history 

@history
def f(a,b,c,d):
    return a, b, c, d

class Test: 
    def __init__(self,a,b,c,d): 
        self.a = a 
        self.b = b 
        self.c = c 
        self.d = d 

    @history
    def f(a,b,c,d): 
        return f(a,b,c,d) 


def main(): 
    
   f(1,2,3,4) 
   print(f.RV,f.T)

   t = Test(1,2,3,4) 
   t.f(1,2,3,4) 
   t.f(4,44,2,4)

if __name__ == "__main__": 
    main() 
