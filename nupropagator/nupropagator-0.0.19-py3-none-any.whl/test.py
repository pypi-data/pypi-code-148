from types import SimpleNamespace
opts = SimpleNamespace()
opts.neutrinoPrimary_energy_mode = 'random'
opts.neutrinoPrimary_direction_mode = 'random'
opts.neutrinoPrimary_target_mode = 'random'
opts.neutrinoPrimary_current_mode = 'random'
opts.neutrinoPrimary_pdgid = 14
opts.neutrinoPrimary_energy_GeV = 10**2 
opts.neutrinoPrimary_direction = [0,0,1]
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.neutrinoPrimary_target = 2212

import nupropagator.nugen as  nugen
import numpy as np



nu = nugen.NuGen()
print('start')
nu.get_event(opts)
print('end')
