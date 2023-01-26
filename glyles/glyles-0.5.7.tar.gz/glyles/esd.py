from glyles import Glycan

g1 = Glycan("Fuc(a1-4)Gal(a1-4)Man")
g1.create_snfg_img("g1.png")
print(g1.get_smiles())

g2 = Glycan("Fuc(a1-4)[Tal(a1-3)]Gal(a1-4)Man")
g2.create_snfg_img("g2.png")
print(g2.get_smiles())
