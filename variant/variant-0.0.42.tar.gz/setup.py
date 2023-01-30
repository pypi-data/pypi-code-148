# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['variant']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.0,<2.0.0',
 'pyensembl>=2.2.4,<3.0.0',
 'rich-click>=1.6.0,<2.0.0',
 'varcode']

entry_points = \
{'console_scripts': ['variant-effect = variant.effect:run']}

setup_kwargs = {
    'name': 'variant',
    'version': '0.0.42',
    'description': '',
    'long_description': '# Python pakcage for genomic variant analysis\n\n[![Pypi Releases](https://img.shields.io/pypi/v/variant.svg)](https://pypi.python.org/pypi/variant)\n[![Downloads](https://pepy.tech/badge/variant)](https://pepy.tech/project/variant)\n\n## How to use?\n\n```\npip install variant\n```\n\n- run `variant-effect` in the command line\n- more functions will be supported in the future\n\n## `variant-effect` command can infer the effect of a mutation\n\n```\n Usage: variant-effect [OPTIONS]\n\n Variant (genomic variant analysis in python)\n\n╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --input                 -i  TEXT       Input position file.                                                          │\n│ --output                -o  TEXT       Output annotation file                                                        │\n│ --reference             -r  TEXT       reference species                                                             │\n│ --reference-gtf             TEXT       Customized reference gtf file.                                                │\n│ --reference-transcript      TEXT       Customized reference transcript fasta file.                                   │\n│ --reference-protein         TEXT       Customized reference protein fasta file.                                      │\n│ --release               -e  INTEGER    ensembl release                                                               │\n│ --type                  -t  [DNA|RNA]  (deprecated)                                                                  │\n│ --strandness            -s             Use strand infomation or not?                                                 │\n│ --pU-mode               -u             Make rRNA, tRNA, snoRNA into top priority.                                    │\n│ --npad                  -n  INTEGER    Number of padding base to call motif.                                         │\n│ --all-effects           -a             Output all effects.                                                           │\n│ --with-header           -H             With header line in input file.                                               │\n│ --columns               -c  TEXT       Sets columns for site info. (Chrom,Pos,Strand,Ref,Alt) [default: 1,2,3,4,5]   │\n│ --help                  -h             Show this message and exit.                                                   │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\n> demo:\n\nStore the following table in file (`sites.tsv`).\n\n|       |           |     |     |     |\n| :---- | :-------- | :-- | :-- | :-- |\n| chr1  | 230703034 | -   | C   | T   |\n| chr2  | 215361150 | -   | A   | T   |\n| chr2  | 84906537  | +   | C   | T   |\n| chr3  | 10301112  | -   | G   | T   |\n| chr3  | 20301112  | -   | G   | T   |\n| chr7  | 45893389  | +   | G   | T   |\n| chr7  | 94669540  | +   | G   | N   |\n| chr12 | 69353439  | +   | A   | T   |\n| chr14 | 23645352  | +   | G   | T   |\n\nRun command `variant-effect -i sites.tsv -r human -e 106 -t RNA` to get the following output.\n\n| #chrom | pos       | strand | ref | alt | mut_type      | gene_name               | gene_pos | transcript_name             | transcript_pos | transcript_motif      | coding_pos | codon_ref | aa_pos | aa_ref | distance2splice |\n| :----- | :-------- | :----- | :-- | :-- | :------------ | :---------------------- | :------- | :-------------------------- | :------------- | :-------------------- | :--------- | :-------- | :----- | :----- | :-------------- |\n| chr1   | 230703034 | -      | G   | A   | ThreePrimeUTR | ENSG00000135744(AGT)    | 42543    | ENST00000680041(AGT-208)    | 1753           | TGTGTCACCCCCAGTCTCCCA | None       | None      | None   | None   | 295             |\n| chr2   | 215361150 | -      | T   | A   | ThreePrimeUTR | ENSG00000115414(FN1)    | 74924    | ENST00000323926(FN1-201)    | 8012           | GGCCCGCAATACTGTAGGAAC | None       | None      | None   | None   | 476             |\n| chr2   | 84906537  | +      | C   | T   | ThreePrimeUTR | ENSG00000034510(TMSB10) | 882      | ENST00000233143(TMSB10-201) | 327            | CCTGGGCACTCCGCGCCGATG | None       | None      | None   | None   | 148             |\n| chr3   | 10301112  | -      | C   | A   | Silent        | ENSG00000157020(SEC13)  | 20001    | ENST00000397117(SEC13-209)  | 1441           | TTGATCATCTGCCTTAACGTG | 849        | CTG       | 283    | L      | 35              |\n| chr3   | 20301112  | -      | C   | A   | Intergenic    | None                    | None     | None                        | None           | None                  | None       | None      | None   | None   | None            |\n| chr7   | 45893389  | +      | G   | T   | ThreePrimeUTR | ENSG00000146678(IGFBP1) | 5030     | ENST00000275525(IGFBP1-201) | 1243           | CAAAGCTCCTGCGTCTGTTTT | None       | None      | None   | None   | 429             |\n| chr7   | 94669540  | +      | G   | N   | ThreePrimeUTR | ENSG00000242265(PEG10)  | 13216    | ENST00000612941(PEG10-206)  | 6240           | TTTTACCCCTGTCAGTAGCCC | None       | None      | None   | None   | 5030            |\n| chr12  | 69353439  | +      | A   | T   | ThreePrimeUTR | ENSG00000090382(LYZ)    | 5059     | ENST00000261267(LYZ-201)    | 695            | TAGAACTAATACTGGTGAAAA | None       | None      | None   | None   | 286             |\n| chr14  | 23645352  | +      | G   | T   | ThreePrimeUTR | ENSG00000100867(DHRS2)  | 15238    | ENST00000344777(DHRS2-202)  | 1391           | CTGCCATTCTGCCAGACTAGC | None       | None      | None   | None   | 210             |\n\n## TODO:\n\n- imporve speed. Base on [cgranges](https://github.com/lh3/cgranges), [pyranges](https://github.com/biocore-ntnu/pyranges)?, or [BioCantor](https://github.com/InscriptaLabs/BioCantor)?\n',
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yech1990/variant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
