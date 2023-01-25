"""
Module for interacting programs remotely using CGI
"""

import cgi
import subprocess


class CGIInterfacing:
    """
    Class for interacting with python scripts
    present on server using CGI
    """
    def __init__(self):
        self.file_name = None
        self.arguments = None
        self.form = None

    def create_cgi_field(self):
        """
        creates the field storage instance
        """
        self.form = cgi.FieldStorage()

    def get_form_data(self):
        """
        retrieves the data from the form submitted
        """
        self.file_name = self.form.getvalue('filename')
        self.arguments = self.form.getlist('arguments')

    def get_results(self):
        """
        executes the python script specified and returns the results
        """
        result = subprocess.getoutput(['python', self.file_name] + self.arguments)
        result = result.decode('utf-8').strip('\n')
        print("Content-type:text/html\r\n\r\n")
        print("<html>")
        print("<head>")
        print("<title>CGI Interfacing</title>")
        print("</head>")
        print("<body>")
        print("<h2>The Output of the program is: -</h2>")
        print(f"<h5>{result}</h5>")
        print("</body>")
        print("</html>")
