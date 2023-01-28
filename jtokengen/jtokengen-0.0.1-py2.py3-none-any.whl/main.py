from uuid import uuid4
import sys

# GENERAMOS EL TOKEN DINÁMICAMENTE
rand_token = uuid4()
print(rand_token)

# OBTENEMOS EL PATH PARA EL ARCHIVO DE DONDE SE ALMACENA EL TOKEN
path = sys.argv[1]
print(path)

# GENERAMOS EL ARCHIVO DE TOKEN EN LA RUTA ESTABLECIDA
oftoken = open(path, "w+")
oftoken.write(str(rand_token))