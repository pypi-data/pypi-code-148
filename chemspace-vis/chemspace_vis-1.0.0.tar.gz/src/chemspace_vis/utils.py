import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw


def read_fingerprints(fn, smi_fn=None):
    if smi_fn is None:
        assert fn.endswith('.fp')
        smi_fn = fn[:-3] + '.smi'
    mol_ids = []
    with open(smi_fn) as f:
        lines = f.readlines()
    for line in lines:
        ll = line.strip().split()
        if len(ll) > 1:
            mol_ids.append(ll[-1])
    with open(fn) as f:
        lines = f.readlines()
    bytes_list = []
    for line in lines:
        if line.startswith('fingerprint = '):
            fp = line.strip().split(' = ')[-1].split('|')
        elif line.startswith('0') or line.startswith('1'):
            fp = line.strip().split('|')
        else:
            continue
        fp_binary = []
        for bits in fp:
            if len(bits) == 8:
                fp_binary += [int(x) for x in bits]
            elif len(bits) > 0:
                raise ValueError("Wrong format for .fp file (not packets of 8 bits separated by |)")
        bytes_list.append(np.packbits(np.array(fp_binary)))
    np_fps = np.zeros((len(bytes_list), 128), dtype=np.uint8)
    for i, b in enumerate(bytes_list):
        np_fps[i] = b
    if len(mol_ids) != len(np_fps):
        raise ValueError("Error: {} mol_ids from .smi file, {} fingerprints from .fp file".format(len(mol_ids),
                                                                                                  len(np_fps)))
    return np.unpackbits(np_fps, axis=1), mol_ids


def draw_mol_from_smiles(smiles_str, filename, mol_id=""):
    mol = Chem.MolFromSmiles(smiles_str)
    img = Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(400, 400), legends=[mol_id])
    img.save(filename)


def get_hac_from_smiles(smiles_str):
    mol = Chem.MolFromSmiles(smiles_str)
    return len(mol.GetAtoms())

