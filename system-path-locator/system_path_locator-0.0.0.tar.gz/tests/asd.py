import os
import sys

def locate(repo_name):

    if type(repo_name) == str:

        disco_entero = os.getcwd()
        workspace = ''

        # si ejecuto el test desde cualquier posicion de cmd, y si no le paso custom params
        if not bool(disco_entero.__contains__(repo_name)) and len(sys.argv) == 1:
            new_path = ''
            arg_path = sys.argv[0]
            directories = arg_path.split('\\')

            for directory in directories:
                if directory == repo_name:
                    workspace = new_path[1:]
                    sys.path.append(workspace)
                    return workspace 

                else:
                    new_path = new_path + '\\' + directory

        # si digo especifocamente la ruta del repo un nivel arriba
        elif len(sys.argv) > 2 and sys.argv[1] == '--custom-path':
            custom_path = sys.argv[2]
            sys.path.append(custom_path)
            return custom_path

        # si el disco donde estoy parado no tiene el repo ej: C:\automation
        elif disco_entero[:13] != disco_entero[:3] + repo_name:
            directories = disco_entero.split('\\')
            new_path = ''

            for directory in directories:
                if directory == repo_name:
                    workspace = new_path[1:]
                    sys.path.append(workspace)
                    return workspace

                else:
                    new_path = new_path + '\\' + directory

        # por descarte el repo esta al lado del disco, C:\automation
        else:
            workspace = disco_entero[0:3]
            sys.path.append(workspace)
            return workspace
    else:
        raise TypeError("The param for locate(repo_name) must be 'string'")
