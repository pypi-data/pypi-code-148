from uuid import uuid4
import sys

class jtokengen:
    def start(self):
        # GENERAMOS EL TOKEN DINÁMICAMENTE
        rand_token = uuid4()

        # OBTENEMOS EL PATH PARA EL ARCHIVO DE DONDE SE ALMACENA EL TOKEN
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = "token.txt"
        # MOSTRAMOS EL PATH A UTILIZAR
        print(f"{rand_token}")
        # GENERAMOS EL ARCHIVO DE TOKEN EN LA RUTA ESTABLECIDA
        oftoken = open(path, "w+")
        oftoken.write(str(rand_token))

# EJECUCIÓN PRINCIPAL DE LA LÓGICA
if __name__ == "__main__":
    ojtokengen = jtokengen()
    ojtokengen.start()
