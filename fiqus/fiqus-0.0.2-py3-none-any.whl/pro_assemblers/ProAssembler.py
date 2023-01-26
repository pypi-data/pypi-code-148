from fiqus.pro_templates import combined
from jinja2 import Environment, FileSystemLoader


class ASS_PRO:
    def __init__(self, file_base_path, naming_conv=None):
        """
        Class for generating pro templates
        :param file_base_path: this is a full path to a folder with the model and includes model name, but without extension
        :param naming_conv: a dictionary with naming convention for regions in .pro file. Optional parameter, as a default below is used, but it could be overwritten if needed.
        """
        self.file_base_path = file_base_path
        if not naming_conv:
            self.naming_conv = {'omega': 'Omega', 'terms': 'Terms', 'bd': 'Bd', 'cond': '_c', 'powered': '_p', 'induced': '_i', 'air': '_a', 'line': 'Line'}
        else:
            self.naming_conv = naming_conv

    def assemble_combined_pro(self, template, rm, dm, BH_curves_path: str = ''):
        """
        Generates model .pro file from .pro template and regions model (rm)
        :param BH_curves_path: path of the BH curves pro file
        :param template: .pro template file name
        :param rm: regions model data structure (yaml loaded to regions data model)
        :param dm: data model structure
        :return: None. Generates .pro file and saves it on disk in the model folder under model_name.pro
        """
        loader = FileSystemLoader(combined.__path__)
        env = Environment(loader=loader, variable_start_string='<<', variable_end_string='>>',
                          trim_blocks=True, lstrip_blocks=True)
        env.globals.update(zip=zip)  # this is to pass python zip function to the template, as normally it is not available. It should work for passing any python function that is not available in .pro template.
        pro_template = env.get_template(template)
        output_from_parsed_template = pro_template.render(BHcurves=BH_curves_path, rm=rm, dm=dm, nc=self.naming_conv)
        with open(f"{self.file_base_path}.pro", "w") as tf:
            tf.write(output_from_parsed_template)

    def assemble_separate_pro(self, template, rm, dm, BH_curves_path: str = ''):
        """
        This function is not developed yet.
        """
        pass
