import nbformat
import argparse
from nb_nodes import Nodes


def nbformat_to_ipynb(out_path, nb):
    with open(out_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


def ipynb_to_nbformat(in_path):
    with open(in_path) as f:
        return nbformat.read(f, as_version=4)


def make_notebook(enterprise_nlp_secret: str, out_path: str, base_notebook_path: str) -> None:
    """Generate Notebook which can be used to test out new Secret
    :param enterprise_nlp_secret: NLP Secret
    :param out_path: Where to output notebook & file name for it
    :param base_notebook_path: Path to base notebook to use
    """
    Nodes.auth_with_jsl_lib['source'] = Nodes.auth_with_jsl_lib['source'].replace('<SECRET>', enterprise_nlp_secret)
    nb = ipynb_to_nbformat(base_notebook_path)
    for inject_node in [Nodes.auth_with_jsl_lib, Nodes.get_sample_text_df]:
        nb['cells'].insert(len(nb['cells']), inject_node)
    nbformat_to_ipynb(out_path, nb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=""" 
    JSL-Test Notebook Generator. Call 
    python generate_notebook.py --secret=my_secret 
    python generate_notebook.py --secret=my_secret --out_path=/put/my/notebook/here.ipynb 
    python generate_notebook.py --secret=my_secret --out_path=/put/my/notebook/here.ipynb --base_notebook=use/this/as/base/notebook.ipynb 
    """, )
    parser.add_argument("--secret", required=True,
                        help='The secret to use for generating the notebook')
    parser.add_argument("--out_path", required=False,
                        help='Output Path for notebook, including the name of notebook to output')
    parser.add_argument("--base_notebook", required=False,
                        help='Path to base notebook file to use to generate notebook')
    args = parser.parse_args()
    if not args.out_path:
        args.out_path = 'test_notebook.ipynb'
    if not args.base_notebook:
        args.base_notebook_path = 'base_notebook.ipynb'

    print(f'Creating notebook in {args.out_path} with secret {args.secret}')
    make_notebook(args.secret, args.out_path, args.base_notebook_path)
