from pymol import cmd
from pymolstyles.external.cgo_arrow import *

import ast

def plot_vdw(arg1):
    cmd.copy(arg1+"_vdw", arg1)
    cmd.set("sphere_scale",1.0, arg1+"_vdw and elem H")
    cmd.rebuild()
    cmd.set("sphere_scale", 1, arg1+"_vdw")
    cmd.hide("nonbonded", arg1+"_vdw")
    cmd.hide("lines", arg1+"_vdw")
    cmd.hide("sticks", arg1+"_vdw")
    cmd.set("sphere_transparency", 0.5, arg1+"_vdw")
cmd.extend("plot_vdw", plot_vdw)

def plot_cube(isovalue=0.004):
    '''
    todo --> orbital cube must be imported first, then the structure (bug)
    '''
    cmd.set("internal_gui_width", 525)
    obj_list = cmd.get_names('objects')
    print(obj_list)
    isovalue = float(isovalue)
    for cube in obj_list:
        orbitalName = 'orb-'+cube
        positiveOrbital = cube+'+'
        negativeOrbital = cube+'-'
        
        cmd.isosurface(positiveOrbital,cube,isovalue*1)
        cmd.color("blue",positiveOrbital) 
        cmd.isosurface(negativeOrbital,cube,isovalue*-1)
        cmd.color("red",negativeOrbital)

        for orbital in (positiveOrbital,negativeOrbital):
            cmd.group(orbitalName, orbital)
cmd.extend("plot_cube", plot_cube)

def plot_nci(arg1, isovalue=0.3):
	# nci.py, a tiny script to display plots from Nciplot in PyMOL
    densf = arg1+"-dens"
    gradf = arg1+"-grad"
    cmd.isosurface("grad",gradf, isovalue)
    cmd.ramp_new("ramp", densf, [-5,5], 'rainbow')
    cmd.set("surface_color", "ramp", "grad")
    cmd.set('transparency', 0, 'grad')
    cmd.set('two_sided_lighting',value=1)
cmd.extend( "plot_nci", plot_nci)

def plot_elpot(arg1, isovalue=0.04, scale=0.5):
    densf = arg1+"_dens"
    gradf = arg1+"_esp"
    min_surface, max_surface = [abs(float(scale))*-1, abs(float(scale))]
    cmd.isosurface("dens",densf, isovalue)
    cmd.ramp_new("ramp", gradf, [min_surface, max_surface], 'rainbow')
    cmd.set("surface_color", "ramp", "dens")
    cmd.set('transparency', 0.50, 'dens')
    cmd.set('two_sided_lighting',value=1)
cmd.extend("plot_elpot", plot_elpot)

def plot_sterimol(origin, sterimol_coordinates):
    cmd.delete('*_vector')

    origin = ast.literal_eval(origin)
    sterimol_coordinates = ast.literal_eval(sterimol_coordinates)

    cmd.pseudoatom('c', pos=origin, elem='Cs')
    cmd.pseudoatom('L', pos=sterimol_coordinates[0], elem='Cs')
    cmd.pseudoatom('B1', pos=sterimol_coordinates[1], elem='Cs')
    cmd.pseudoatom('B5', pos=sterimol_coordinates[2], elem='Cs')

    cgo_arrow('/c','/L', 0.1, color='red', name='L_vector')
    cgo_arrow('/c','/B1', 0.1, color='green', name='B1_vector')
    cgo_arrow('/c','/B5', 0.1, color='blue', name='B5_vector')

    cmd.delete('c')
    cmd.delete('L')
    cmd.delete('B1')
    cmd.delete('B5')
cmd.extend('plot_sterimol', plot_sterimol)


def plot_buried_volume(bv_name, color='lightblue', radius=3.5):
    '''
    USAGE
        buriedvolume bv_name, color='lightblue', radius=3.5)
    '''
    cmd.pseudoatom(bv_name, selection='sele', vdw=radius)
    cmd.hide('wire', bv_name)
    cmd.show('spheres', bv_name)
    cmd.set('sphere_transparency', 0.5, bv_name, )
    cmd.color(color, bv_name)
cmd.extend('plot_buried_volume', plot_buried_volume)