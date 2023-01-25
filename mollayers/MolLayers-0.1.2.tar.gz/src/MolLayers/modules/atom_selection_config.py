from Bio.PDB import Select

#Autoselects the atoms based on the layer number assigned to the atom
class SelectLayer(Select):
    def __init__(self,layer_number):
        self.layer_number=layer_number
    def accept_atom(self,atom):
        if atom.disordered_flag==0 and atom.layer_number==self.layer_number:
            return True
        else:
            return False
#Selects atoms that are labelled as surface
class SelectSurface(Select):
    def accept_atom(self,atom):
        if atom.disordered_flag==0 and atom.is_surface:
            return True
        else:
            return False

