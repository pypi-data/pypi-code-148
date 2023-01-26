import scanpy as sc
import pickle as pkl

def save_pickle_file(file_path, data):
    with open(file_path, 'wb') as f:
        pkl.dump(data, f)

def read_pickle_file(file_path):
    with open(file_path, 'rb') as f:
        return pkl.load(f)

def get_gene_list(train_df):
    genes = train_df.iloc[:,1:-1]
    labels = train_df.iloc[:,-1:]
    train = sc.AnnData(genes, labels)
    celltypes_list = train.obs.celltype.unique().tolist()
    sc.pp.log1p(train)
    sc.tl.rank_genes_groups(train, groupby="celltype")
    # sc.pl.rank_genes_groups(train, groupby="celltype")
    top_50_DE_genes = {c: [] for c in celltypes_list}
    for c in top_50_DE_genes:
        detrain_df = sc.get.rank_genes_groups_df(train, group=c).head(50)
        top_50_DE_genes[c] = detrain_df['names'].tolist()
    return top_50_DE_genes

def save_gene_list(train_df, save_path):
    genes = train_df.iloc[:,1:-1]
    labels = train_df.iloc[:,-1:]
    train = sc.AnnData(genes, labels)
    celltypes_list = train.obs.celltype.unique().tolist()
    sc.pp.log1p(train)
    sc.tl.rank_genes_groups(train, groupby="celltype")
    # sc.pl.rank_genes_groups(train, groupby="celltype")
    top_50_DE_genes = {c: [] for c in celltypes_list}
    for c in top_50_DE_genes:
        detrain_df = sc.get.rank_genes_groups_df(train, group=c).head(50)
        top_50_DE_genes[c] = detrain_df['names'].tolist()
    save_pickle_file(save_path, top_50_DE_genes)