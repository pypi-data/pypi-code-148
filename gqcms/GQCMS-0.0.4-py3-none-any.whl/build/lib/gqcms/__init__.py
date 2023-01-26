# Basis and matrices
from gqcms.matrices import Determinant
from gqcms.matrices import NumberOperator
from gqcms.matrices import DensityOperator
from gqcms.matrices import basisTransform
from gqcms.matrices import createHamiltonian
from gqcms.matrices  import createHamiltonianSCI
from gqcms.basis import seniorityBasis

# Molecule
from gqcms.Hubbard import Hubbard
from gqcms.Heisenberg import heisenberg

# Methods
from gqcms.DMRG import DMRG
from gqcms.HartreeFock import HartreeFock
from gqcms.ConfigurationInteraction import FCI
from gqcms.ConfigurationInteraction import SCI

# Descriptors
from gqcms.Information import Entropy
from gqcms.Information import EntropyFromDataFrame
from gqcms.Information import MutualInformation
from gqcms.Information import MutualInformationFromDataFrame
from gqcms.MPD import MPD
from gqcms.BondOrderOperator import BondOrderDataFrame
from gqcms.EDF import FullEDF

from gqcms.ConstrainedMethod import ConstrainedFCI
from gqcms.ConstrainedMethod import ConstrainedHartreeFock
from gqcms.ConstrainedMethod import ConstrainedSCI
from gqcms.Scans import LagrangeScan
from gqcms.Scans import ExpectationValueScan

# Math
from gqcms.Optimization import LineSearch
from gqcms.math import derivative

# Plot functions
from gqcms.PlottingTools.Plot import scatter
from gqcms.PlottingTools.Plot import scatterPlots
from gqcms.PlottingTools.Plot import scatterSubPlots
from gqcms.PlottingTools.Plot import applyNotebookStyle
from gqcms.PlottingTools.Plot import applyPaperStyle
from gqcms.PlottingTools.Plot import plot_onv_probability
from gqcms.PlottingTools.Plot import plot_all_onv_probabilities
from gqcms.PlottingTools.Plot import plot_site_probability
from gqcms.PlottingTools.Plot import imshow
from gqcms.PlottingTools.LegendPlotter import CombineFigures
from gqcms.PlottingTools.LegendPlotter import plotDomains
from gqcms.PlottingTools.LegendPlotter import plotONVs

# Diagonalization algorithms
from gqcms.diagonalization.Davidson import Davidson
from gqcms.diagonalization.Lanczos import Lanczos

# Print version information
import subprocess

with subprocess.Popen(
    ["git rev-parse HEAD"], cwd=__file__[:-17], shell=True, stdout=subprocess.PIPE
) as proc:
    print("gqcms @", proc.stdout.read().decode('utf-8').strip('\n'))

    
