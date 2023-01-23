from pymol import cmd

# GUI and color space
cmd.set("internal_gui_width", 400)
cmd.bg_color("white")
cmd.space("cmyk")

# Ray-Trace Settings
cmd.set("ray_trace_mode", 1)
cmd.set("ray_texture", 0)
cmd.set("ray_opaque_background", "off")