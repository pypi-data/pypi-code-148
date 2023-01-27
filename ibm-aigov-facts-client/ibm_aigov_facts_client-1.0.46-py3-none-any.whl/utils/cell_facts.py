import os
import itertools
import logging
from base64 import b64decode,b64encode
from io import BytesIO
from IPython import get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (Magics, cell_magic, magics_class)
from IPython.display import display
from IPython.utils.capture import capture_output

_logger = logging.getLogger(__name__) 

def increment_filename(file_name):
    extension=".html"
    fid, _ = os.path.splitext(file_name)
    yield fid + extension
    for n in itertools.count(start=1, step=1):
        new_id = fid +'_'+ str(n)
        yield "%s%s" % (new_id, extension)

def get_file_path(filename,appendonly=False):
    target_file_path = None
    
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'cell_facts_tmp')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    if appendonly:   
        file_path = os.path.join(final_directory, filename+".html")
        target_file_path = file_path
     
    else:
        for file_name in increment_filename(filename):
            file_path = os.path.join(final_directory, file_name)
            if not os.path.isfile(file_path):
                target_file_path = file_path
                break
    return target_file_path

@magics_class
class CellFactsMagic(Magics):

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "--filename",
        "-f",
        default=None,
        help=("The file name to save with"),
    )
    @magic_arguments.argument(
        "--saveonly",
        "-s",
        action='store_true',
        help=("Defines whether to save and export or just save the file"),
    )
    @magic_arguments.argument(
        "--appendonly",
        "-a",
        action='store_true',
        help=("Defines whether to append all results in one file"),
    )
    @magic_arguments.argument(
        "--printmsgonly",
        "-po",
        action='store_true',
        help=("Defines whether to capture print messages only"),
    )

    @magic_arguments.argument(
        "--capturecode",
        "-cc",
        action='store_true',
        help=("Defines whether to capture cell codes"),
    )
    
    def capture_cell_facts(self, line, cell):
        args = magic_arguments.parse_argstring(CellFactsMagic.capture_cell_facts, line)
        filename=None
        if args.filename:
            filename = args.filename.strip('"')
        save_only = args.saveonly
        stdout_only = args.printmsgonly
        cap_codes=args.capturecode
        append_only=args.appendonly
        
        fmt='''<div class="card"><img src="data:image/png;base64,{}"/><br>\n'''
        txt='''<pre> {} </pre> <br>\n'''
        t='''<p> {} </p> <br>\n'''
        tmp=[]


        f_name=filename or "tmp_output"

        output_filename= get_file_path(f_name,append_only)


        with capture_output(stdout=True, stderr=False, display=True) as io:
            get_ipython().run_cell(cell)
        io()
        
        if stdout_only:
            with capture_output(stdout=True, stderr=False, display=True) as result:
                #self.shell.run_cell(cell)
                get_ipython().run_cell(cell)
                with open(output_filename, 'a+') as fd:
                    if result.stdout is not None:
                        message=result.stdout
                        fmt_data="<br />".join(message.split("\n"))
                        if cap_codes:
                            fmt_cell="<br />".join(cell.split("\n"))
                            fd.write(t.format(fmt_cell))
                        fd.write(t.format(fmt_data))
                _logger.info("Saved cell facts under file {} ".format(output_filename))
                
        else:
            with capture_output(stdout=False, stderr=False, display=True) as result:
                #self.shell.run_cell(cell)
                get_ipython().run_cell(cell)
                if result.outputs:
                    for output in result.outputs:
                        data = output.data
                        tmp.append(data)


            with open(output_filename, 'a+') as fd:
                if cap_codes:
                    fmt_cell="<br />".join(cell.split("\n"))
                    fd.write(t.format(fmt_cell))

                for i in tmp:
                    if 'image/png' in i:
                        png_bytes = i['image/png']
                        if isinstance(png_bytes, str):
                            png_bytes = b64decode(png_bytes)
                        assert isinstance(png_bytes, bytes)
                        bytes_io = BytesIO(png_bytes)
                        encoded_string = b64encode(bytes_io.getvalue()).decode()
                        img_str=fmt.format(encoded_string)
                        fd.write(img_str)

                    elif 'text/plain' in i and not 'text/html' in i:
                        txt_data = i['text/plain']
                        fd.write(txt.format(txt_data))
                    
                    elif 'text/plain' in i and 'text/html' in i:
                        tbl_data = i['text/html']
                        fd.write(tbl_data)
                    
                    else:
                        fmt_data="<br />".join(i.split("\n"))
                        fd.write(t.format(fmt_data))

            _logger.info("Saved cell facts under file {} ".format(output_filename))