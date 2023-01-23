from pymol import cmd

def save_img(filename='default', ray_mode=1):
    '''
    Export the current workspace as PNG using Ray-Tracing. If filename is not present
    the image is named default.png, except if only one element is visible in the workspace.
    In this case the filename is the same as the name of the visible entry.
    '''
    visible_entries = cmd.get_object_list(selection='visible')
    if filename == 'default' and len(visible_entries) == 1:
        filename = visible_entries[0]

    screen_size = cmd.get_viewport(output=1, quiet=1)
    canvas_width = screen_size[0]
    canvas_height = screen_size[1]

    cmd.set("ray_trace_gain", 8) # Increase ray_trace_gain for improved look on the final image
    cmd.png(filename, canvas_width*3, canvas_height*3, dpi=300, ray=ray_mode)
    cmd.set("ray_trace_gain", 0.12) # Reset ray_trace_gain back to default
cmd.extend("save_img",save_img)

def group_visible(groupname='test', include_measurements=False):
    visible_entries = cmd.get_object_list(selection='visible')
    if include_measurements:
        all_objects = cmd.get_names(type='all')
        for item in all_objects:
            dist_obj = re.search('dist([0-9]{1,4})', item)
            if dist_obj:
                dist_obj_id = dist_obj.group(1)
                dist_obj_newname = f"{visible_entries[0]}_dista{dist_obj_id}"
                cmd.set_name(item, dist_obj_newname)
                visible_entries.append(dist_obj_newname)
    cmd.group(groupname, ' '.join(visible_entries))
cmd.extend("group_visible",group_visible)

def bond_between(element1, element2, cutoff=2.3):
    visible_entries = cmd.get_object_list(selection='visible')
 
    for entry in visible_entries:

        bonds = cmd.find_pairs(
            f"element {element1} and {entry}", 
            f"element {element2} and {entry}", 
            cutoff=cutoff)
        print(f"{entry} has {len(bonds)} bonds between {element1} and {element2}")
        
        for bond in bonds:
            entry = bond[0][0]
            element1_id = bond[0][1]
            element2_id = bond[1][1]
            cmd.bond(f"id {element1_id} and {entry}", f"id {element2_id} and {entry}")
cmd.extend("bond_between",bond_between)

def align_visible(reference_entry_id=0):
    visible_entries = cmd.get_object_list(selection='visible')
    reference_entry = visible_entries[reference_entry_id]
    mobile_entries = [i for i in visible_entries if i != reference_entry]
    for entry in mobile_entries:
        cmd.align(entry, reference_entry, cycles=200)
cmd.extend("bond_between",bond_between)

def quick_overlay(entry, color='blue'):
    cmd.color(color,entry)
    cmd.set('stick_transparency', 0.5, entry)
    cmd.set('sphere_transparency', 0.5, entry)
cmd.extend('quick_overlay', quick_overlay)
cmd.extend("bond_between",bond_between)
