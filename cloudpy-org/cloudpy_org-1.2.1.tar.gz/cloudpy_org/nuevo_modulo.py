class myNuevaClase:
    def __init__(self):
        ...
    def unaFuncionQueInvente(self,unNombre:str="Sin Nombre")->str:
        '''
        ***
        Es una función que dado un nombre, saluda al mismo y le pregunta cómo está.
        ***
        '''
        return "Hola " + unNombre + ", cómo estás."
    
    def unaSuma(self,a:int=0,b:int=0)->int:
        '''
        ***
        Da la suma de dos números enteros dados.
        ***
        '''
        return a + b
    def unaMultiplicación(self,a:float,b:float)->float:
        '''
        ***
        Regresa el producto de dos números dados
        ***
        '''
        return a*b
    