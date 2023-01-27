import os
import shutil
import jinja2
import pdfkit
import tempfile
import pandas as pd
import numpy as np
from pathlib import Path

def render_pdf(xlsfile=None, output_dir=None, template_file=None, path_wkhtmltopdf=os.path.expanduser("~")+"\\wkhtmltopdf\\bin\\wkhtmltopdf.exe", options=None, default_value="n. d."):
    if None in (xlsfile, output_dir, template_file):
        raise Exception("One or multiple required variables are missing...")
    
    # Set variables
    pdfkitconfig = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    if options == None:
        options = { 
            'page-size': 'Letter',
            'margin-top': '0.35in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
    
    # Read xls
    df = pd.read_excel(xlsfile, dtype=str, sheet_name=0, engine='openpyxl')
    id = df.columns[0]
    
    if pd.Series(df[id]).is_unique == False or pd.Series(df[id]).isnull().values.any():
        raise Exception("ERROR: ID column is not unique or contains empty values...")
    
    # Define custom functions
    def numb(value):
        """Applies thousands separator to floats, with 2 decimal places."""
        if value=="." or value=="": 
            return default_value
        else: 
            numb = round(float(value), 0)
            if np.isnan(numb): return default_value
            else: return '{:,.0f}'.format(float(numb)).replace(',','.')

    def perc(value):
        if value=="." or value=="":
            return default_value
        else: 
            perc = round(float(value) * 100, 1)
            if np.isnan(perc): return default_value
            else: return '{:,.1f}'.format(float(perc)).replace(",", "_").replace(".", ",").replace("_", ".") +" %"

    def euro(value):
        if value=="." or value=="": 
            return default_value
        else: 
            euro = round(float(value), 2)
            if np.isnan(euro): return default_value
            else: return '{:,.2f}'.format(float(euro)).replace(",", "_").replace(".", ",").replace("_", ".") +" €"

    custom_func_dict = {"numb": numb,
                        "perc": perc,
                        "euro": euro,}

    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_file))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(os.path.basename(template_file))
    template.globals.update(custom_func_dict)

    # Create output directory if needed
    Path(output_dir).mkdir( parents=True, exist_ok=True )

    # Clean up output directory
    all_files = os.listdir(output_dir)
    only_pdf_files = [file for file in all_files if ".pdf" in file]
    if len(only_pdf_files)>0 and os.path.isdir(os.path.join(output_dir, "trash"))==False: 
        os.makedirs(os.path.join(output_dir, "trash"))
    for file in only_pdf_files:
        shutil.move(os.path.join(output_dir, file), os.path.join(output_dir+"\\trash", file))

    # Loop through rows in xls and generate one PDF each
    with tempfile.TemporaryDirectory() as temp_dir:
        for row in df.to_dict(orient="records"):
            kwargs = row
            output_text = template.render(**kwargs)

            # Generate HTML in tempdir
            html_path = f'{temp_dir}\\{row[id]}.html'
            html_file = open(html_path, 'w', encoding="utf-8")
            html_file.write(output_text)
            html_file.close()

            # Convert html to pdf
            pdf_filepath = f'{output_dir}\\{row[id]}.pdf'
            with open(html_path, encoding="utf-8") as f:
                pdfkit.from_file(f, pdf_filepath, options=options, configuration=pdfkitconfig)
