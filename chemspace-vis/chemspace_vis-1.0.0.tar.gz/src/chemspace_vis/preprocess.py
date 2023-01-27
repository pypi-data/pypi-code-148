from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from chemspace_vis.chembl import read_csv_activity, ChemblActivity
from chemspace_vis.utils import read_fingerprints, draw_mol_from_smiles
import numpy as np
import os


def preprocess_chembl(csv_filename, activity_name, max_hac=30, max_mw=500, smi_fn=None, df_fn=None,
                      img_folder="mol_images"):
    assert csv_filename.endswith('.csv')
    ch_act = read_csv_activity(csv_filename, activity=activity_name)
    assert isinstance(ch_act, ChemblActivity)
    if smi_fn is None:
        smi_fn = csv_filename[:-4] + ".smi"
    if df_fn is None:
        df_fn = csv_filename[:-4] + "_activity.df"
    ch_act.generate_id_activity_df(df_fn, use_mean=True, hac_filter=max_hac)
    ch_act.generate_smiles_id_file(smi_fn, mw_thresh=max_mw, hac_thresh=max_hac)
    generate_images(smi_fn, img_folder, df_fn)


def generate_images(smi_fn, img_folder, activity_fn):
    if not os.path.isdir(img_folder):
        os.mkdir(img_folder)
    with open(smi_fn) as f:
        lines = f.readlines()
    with open(activity_fn) as f:
        act_lines = f.readlines()[1:]
    for i, line in enumerate(lines):
        smiles, molid = line.strip().split()
        activity = float(act_lines[i].split()[-1])
        draw_mol_from_smiles(smiles, "{}/{}.png".format(img_folder, molid), molid + "  {:.2f}".format(activity))


def make_tsne_from_fingerprints(fingerprints_fn, smi_fn=None, n_pca_components=180, out_filename="tsne_data.df"):
    fps, mol_ids = read_fingerprints(fingerprints_fn, smi_fn=smi_fn)
    pca = PCA(n_components=n_pca_components)
    pcs = pca.fit_transform(fps)
    print("{:.1f}% of variance explained by the first {} PCs".format(np.sum(pca.explained_variance_ratio_)*100,
                                                                     n_pca_components))
    mod = TSNE(init='random', learning_rate='auto')
    mod.fit(pcs)
    print(len(mod.embedding_))
    with open(out_filename, "w") as f:
        f.write("mol_id embed_x embed_y\n")
        embeds = mod.embedding_
        for i in range(len(mol_ids)):
            mol_id = mol_ids[i]
            f.write("{} {} {}\n".format(mol_id, embeds[i][0], embeds[i][1]))

