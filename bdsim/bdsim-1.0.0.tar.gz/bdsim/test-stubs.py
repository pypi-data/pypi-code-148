import bdsim

sim = bdsim.BDSim(animation=True)  # create simulator
bd = sim.blockdiagram()

g = bd.GAIN()
p = bd.PROD()
