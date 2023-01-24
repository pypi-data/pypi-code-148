import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba de la nueva version")

def generarArray(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self) -> None:
        print("Hola, te saludo desde Saludo.__init__()")


