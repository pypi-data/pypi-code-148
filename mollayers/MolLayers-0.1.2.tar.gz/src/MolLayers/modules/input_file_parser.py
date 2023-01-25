from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.mmtf import MMTFParser
import Bio

#This is reliant on the BioPython module, only the parsers provided by biopython are used
#Automatically selects the necessary parser based on the extension of the input file.
class ParseInputFile():
    def __init__(self,file_name):
        self.atoms=[]
        #If file is already parsed by user and the variable is submitted
        #The following statement will check for it's instance type and
        #call the suitable function
        if isinstance(file_name, Bio.PDB.Structure.Structure):
            self.structure_data=file_name
            self.input_file_extension='pdb'
            self.input_file_id=file_name._id
            self.input_file_name=file_name._id
        else:
            self.input_file_name=file_name
            self.input_file_extension = file_name.split('.')[-1]
            self.input_file_id = file_name.split('/')[-1].split('.')[0]

            self.parse_structure()
        self.init_structure()

    def init_structure(self):
        for atom in self.structure_data[0].get_atoms():
            atom.layer_number = None
            self.atoms.append(atom)
    def parse_structure(self):

        if self.input_file_extension in ['pdb', 'ent']:
            self.structure_data = PDBParser(PERMISSIVE=True, QUIET=True).get_structure(self.input_file_id,
                                                                                       self.input_file_name)

        elif self.input_file_extension in ['pqr']:
            self.structure_data = PDBParser(PERMISSIVE=1, is_pqr=True).get_structure(self.input_file_id,
                                                                                     self.input_file_name)
        elif self.input_file_extension in ['cif']:
            self.structure_data = MMCIFParser(QUIET=True).get_structure(self.input_file_id, self.input_file_name)
        elif self.input_file_extension in ['mmtf']:
            self.structure_data = MMTFParser.get_structure(self.input_file_name)
            # self.structure_data=MMTFParser.get_structure_from_url(input_file_id)

