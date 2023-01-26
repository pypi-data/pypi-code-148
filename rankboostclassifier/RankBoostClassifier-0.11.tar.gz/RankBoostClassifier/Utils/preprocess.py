import scanpy as sc
  
def preprocess(genes, labels, min_genes = 200, min_cells = 20, target_sum = 1e6, n_top_genes = 3000, max_value = 10, get_hvgs=True, scale_and_hvgs = True):
        """
        INPUT:
        file_path: path to .h5ad containing scRNA-seq
        """
        ## convert to h5ad
        adata_test = sc.AnnData(genes, labels)

        ## make var names unique
        adata_test.obs_names_make_unique()
        adata_test.var_names_make_unique()

    ## filter cells with count less than 200
        sc.pp.filter_cells(adata_test, min_genes=min_genes)

        ## filter genes with count less than 20
        sc.pp.filter_genes(adata_test, min_cells=min_cells)

        ## normalise data
        sc.pp.normalize_total(adata_test, target_sum=target_sum)

        ## LogNormalise
        if not(scale_and_hvgs):
                return {'data':adata_test}

        if get_hvgs:
                ## Get HVGS
                sc.pp.log1p(adata_test)
                sc.pp.highly_variable_genes(adata_test, n_top_genes = n_top_genes)
                adata_test = adata_test[:, adata_test.var.highly_variable]

                ## scale data
                sc.pp.scale(adata_test, max_value=max_value)
                return {'data' : adata_test, 'hvg': adata_test.var.highly_variable}

        ## scale data
        sc.pp.scale(adata_test, max_value=max_value)
        return {'data':adata_test}


def get_HVGS(genes, labels, n_top_genes = 3000):
        ## convert to h5ad
        adata_test = sc.AnnData(genes, labels)
        sc.pp.highly_variable_genes(adata_test, n_top_genes = n_top_genes)
        adata_test = adata_test[:, adata_test.var.highly_variable]
        return {'data' : adata_test, 'hvg': adata_test.var.highly_variable}