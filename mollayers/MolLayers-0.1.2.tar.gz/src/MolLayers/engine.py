import Bio.PDB.Structure
from Bio.PDB import PDBIO, MMCIFIO
from Bio.PDB.mmtf.mmtfio import MMTFIO

from .modules.channels import x_channel, y_channel, z_channel
from .modules.input_file_parser import ParseInputFile
from .modules.atom_selection_config import SelectLayer

###################################################################
# Layers class that accepts the input file, out_dir and cut_off   #
# to calculate the surface.                                       #
#                                                                 #
# ------------------> Minimalistic Usage <------------------------#
#                                                                 #
# from MolLayers import engine                                    #
# data = engine.Layers('1a2y.pdb')                                  #
# data.calc_surface(peel_layers=True)                             #
##################################################################
class Layers():
    def __init__(self, file_name, out_dir='.', cut_off=1.52,peel_all_layers=False):
        if out_dir.endswith('/'):
            self.out_dir = out_dir
        else:
            self.out_dir = out_dir+'/'

        self.sampling=False
        if isinstance(cut_off,(list,tuple)):
            self.sampling=cut_off
            self.cut_off=1.52
        if isinstance(cut_off,(float,int)):
            self.cut_off = cut_off
            if self.cut_off>1.52:
                self.sampling=[self.cut_off]


        self.peel_all_layers=peel_all_layers
        self.molecule = ParseInputFile(file_name)
        self.calculate_distance_matrix()
        self.run_processing()

    def __label_atoms(self, channel, coordinate_axis,current_layer_number):
        channel.sort(key=lambda atom: atom.coord[coordinate_axis])
        channel[0].layer_number=current_layer_number
        channel[-1].layer_number=current_layer_number

    def calculate_distance_matrix(self):
        self.x_dist_matrix={}
        self.y_dist_matrix={}
        self.z_dist_matrix={}

        for atom1 in self.molecule.atoms:
            self.x_dist_matrix[atom1] = {}
            self.y_dist_matrix[atom1] = {}
            self.z_dist_matrix[atom1] = {}
            for atom2 in self.molecule.atoms:
                self.x_dist_matrix[atom1][atom2]=x_channel(atom1, atom2)
                self.y_dist_matrix[atom1][atom2]=y_channel(atom1, atom2)
                self.z_dist_matrix[atom1][atom2]=z_channel(atom1, atom2)

    def create_channels_and_label_atoms(self):
        for atom1 in self.un_assigned_atoms:
            atom1.x_channel_atoms = []
            atom1.y_channel_atoms = []
            atom1.z_channel_atoms = []
            for atom2 in self.un_assigned_atoms:

                if self.x_dist_matrix[atom1][atom2] <= self.cut_off:
                    atom1.x_channel_atoms.append(atom2)

                if self.y_dist_matrix[atom1][atom2] <= self.cut_off:
                    atom1.y_channel_atoms.append(atom2)

                if self.z_dist_matrix[atom1][atom2] <= self.cut_off:
                    atom1.z_channel_atoms.append(atom2)

            if len(atom1.x_channel_atoms):
                self.__label_atoms(atom1.x_channel_atoms, 0, self.current_layer_number)
            if len(atom1.y_channel_atoms):
                self.__label_atoms(atom1.y_channel_atoms, 1, self.current_layer_number)
            if len(atom1.z_channel_atoms):
                self.__label_atoms(atom1.z_channel_atoms, 2, self.current_layer_number)
    def run_processing(self):
        continue_layer_assignment=True
        self.current_layer_number=0
        while(continue_layer_assignment):
            self.un_assigned_atoms=[]
            for atom in self.molecule.atoms:
                if not atom.layer_number:
                    self.un_assigned_atoms.append(atom)
            if len(self.un_assigned_atoms)==0 or self.peel_all_layers==False:
                continue_layer_assignment=False
            self.current_layer_number+=1
            self.create_channels_and_label_atoms()

        if self.peel_all_layers and not self.sampling:
            self.write_layers()
            self.calc_RTP()


        if self.sampling:
            self.un_assigned_atoms = []
            for atom in self.molecule.atoms:
                if atom.layer_number == 1:
                    self.un_assigned_atoms.append(atom)

            for index,cut_off in enumerate(self.sampling):
                self.cut_off=cut_off
                self.current_layer_number='s'+str(index+1)
                self.create_channels_and_label_atoms()
                self.write_sample()

    def _out_handle(self):
        if self.molecule.input_file_extension in ['pdb', 'ent']:
            io = PDBIO()
        elif self.molecule.input_file_extension in ['cif']:
            io = MMCIFIO()
        elif self.molecule.input_file_extension in ['mmtf']:
            io = MMTFIO()

        return io
    def write_layers(self):
        out_handles = {}
        out_names = {}
        for atom in self.molecule.atoms:
            if atom.layer_number not in out_handles.keys() and not atom.layer_number is None:
                print("Layer number: ", atom.layer_number)
                out_name = self.out_dir + self.molecule.input_file_id + '_surf' + str(
                    atom.layer_number) + '.' + self.molecule.input_file_extension
                out_names[atom.layer_number] = out_name
                out_handles[atom.layer_number] = self._out_handle()
                out_handles[atom.layer_number].set_structure(self.molecule.structure_data)

        for layer_number in out_handles.keys():
            if self.molecule.input_file_extension in ['mmtf']:
                out_handles[layer_number].save(out_names[layer_number], select=SelectLayer(layer_number))
            else:
                out_handles[layer_number].save(out_names[layer_number], select=SelectLayer(layer_number),
                                               preserve_atom_numbering=True)
            print('Finished writing output to file: ', out_names[layer_number])

    def write_sample(self):
        print('Started writing output')
        print('Cut off value is: ',self.cut_off)
        out_name = self.out_dir + self.molecule.input_file_id + '_sampl_'+str(self.cut_off)+'.' + self.molecule.input_file_extension
        io=self._out_handle()
        io.set_structure(self.molecule.structure_data)
        if self.molecule.input_file_extension in ['mmtf']:
            io.save(out_name, select=SelectLayer(self.current_layer_number))
        else:
            io.save(out_name, select=SelectLayer(self.current_layer_number), preserve_atom_numbering=True)

    def calc_RTP(self):
        print('Started writing RTP')
        out_name = self.out_dir + self.molecule.input_file_id + '.RTP'
        out_file = open(out_name,'w')

        fa_out_name=self.out_dir + self.molecule.input_file_id + '.RTPfa'
        fa_out_file = open(fa_out_name, 'w')

        out_file.write('{0:s}{1:s}{2:s}{3:s}\n'.format('#RName', '#RNo.', '#Chain', '#RTP'))
        for model in self.molecule.structure_data:
            for chain in model:
                for residue in chain:
                    if residue.resname == 'HOH' or residue.disordered != 0:
                        continue
                    rtp=0
                    for atom in residue:
                        if rtp < atom.layer_number:
                            rtp = atom.layer_number
                    residue.rtp = rtp
                    out_file.write('{0:<4s}{1:>6d}{2:>3s}{3:>3d}\n'.format(residue.resname, residue._id[1], chain._id, residue.rtp))
                    fa_out_file.write('{}'.format(residue.rtp))

        fa_out_file.close()
        out_file.close()
        print('RTP written into file: ', out_name)






