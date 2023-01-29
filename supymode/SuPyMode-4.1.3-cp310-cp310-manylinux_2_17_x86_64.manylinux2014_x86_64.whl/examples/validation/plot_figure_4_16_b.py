"""
Validation: 0 with Xavier Daxhelet program
==========================================
"""

from MPSPlots.Render2D import Scene2D, Axis, Line
from FiberFusing import Geometry, Fused2, BackGround
from SuPyMode.solver import SuPySolver
from SuPyMode.fibers import HP630, get_silica_index

# ---------------- SuPyMode data ________________________________
wavelength = 1.55e-6

air = BackGround(index=1)

clad = Fused2(
    fiber_radius=60,
    fusion_degree=0.9,
    index=get_silica_index(wavelength=wavelength)
)

fiber_0 = HP630(wavelength=wavelength, position=clad.fiber[0].core)
fiber_1 = HP630(wavelength=wavelength, position=clad.fiber[1].core)


cores = [
    *fiber_0.polygones,
    *fiber_1.polygones
]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='auto-left',
    y_bounds='auto-bottom',
    n=120,
    index_scrambling=0
)

geometry.plot().show()

solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-10,
    max_iter=10000,
    print_iteration=True,
    accuracy=2
)

solver.init_superset(wavelength=1.55, n_step=500, itr_i=1.0, itr_f=0.01)

solver.add_modes(
    sorting='field',
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'symmetric', 'bottom': 'zero'},
    n_computed_mode=5,
    n_sorted_mode=4
)

solver.add_modes(
    sorting='field',
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'anti-symmetric', 'bottom': 'zero'},
    n_computed_mode=5,
    n_sorted_mode=4
)


solver.superset.name_supermodes('LP01', 'LP21', 'LP02', 'LP41', 'LP11', 'LP31', 'LP12', 'LP51')

solver.superset.plot(type='field').show()

figure = Scene2D(unit_size=(8, 5), title='SBB figure 4.16')

ax = Axis(
    row=0,
    col=0,
    y_scale='log',
    x_label='ITR',
    y_label='Adiabatic criterion',
    show_legend=True,
    y_limits=[1e-4, 1]
)

figure.add_axes(ax)

coupling_list = [
    (solver.superset.LP01, solver.superset.LP02, '-', 'blue'),
    (solver.superset.LP01, solver.superset.LP21, '-', 'red'),
    (solver.superset.LP01, solver.superset.LP41, '-', 'orange'),
    (solver.superset.LP11, solver.superset.LP31, '-', 'purple'),
    (solver.superset.LP11, solver.superset.LP12, '-', 'green'),
    (solver.superset.LP11, solver.superset.LP51, '-', 'turquoise')
]

for mode_0, mode_1, line_style, color in coupling_list:
    adiabatic = mode_0.adiabatic.get_values(mode_1)
    artist = Line(x=mode_0.itr_list, y=adiabatic, label=f'{mode_0.stylized_name}-{mode_1.stylized_name}', line_style=line_style, color=color)
    ax.add_artist(artist)


# ---------------- Figure data ________________________________-
# prefix = "./data/"
# data_directory = [
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP02.csv", 'blue'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP21.csv", 'red'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP41.csv", 'orange'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP31.csv", 'purple'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP12.csv", 'green'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP51.csv", 'turquoise')
# ]


# for data_dir, color in data_directory:
#     data = genfromtxt(data_dir, delimiter=',').T
#     artist = Line(x=data[0], y=data[1], line_style="--", color=color)
#     ax.add_artist(artist)

figure.show()


# -
