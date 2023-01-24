#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Mindbaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Convert .csv to .dot
"""

import os;
import sys;
import argparse;
from datetime import datetime, timedelta;
from pprint import pprint;

sys.path.insert ( 0, os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) ) );
from csv_to_dot.csv_to_dot import CsvToDot;
from csv_to_dot import __version__;

def run ():
    parser = argparse.ArgumentParser ( prog = 'csv_to_dot' );
    
    ## All arguments
    parser.add_argument ( '--csv-file', type = str, nargs = '?', help = 'Absolute local path to CSV file to convert' );
    parser.add_argument ( '--csv-delim', type = str, nargs = '?', help = 'CSV delimiter, default : ";"', default = ';' );
    parser.add_argument ( '--dot-file', type = str, nargs = '?', help = 'Absolute local path to DOT file to create' );
    parser.add_argument ( '--nodes-shape', type = str, nargs = '?', help = 'Nodes shape, default : "box"', default = "box" );
    parser.add_argument ( '--nodes-style', type = str, nargs = '?', help = 'Nodes style, default : "filled"', default = "filled" );
    parser.add_argument ( '--nodes-bg-color', type = str, nargs = '?', help = 'Nodes background color, default : "blue"', default = "blue" );
    parser.add_argument ( '--nodes-font-color', type = str, nargs = '?', help = 'Nodes font color, default : "white"', default = "white" );
    parser.add_argument ( '--version', action = 'store_true', help = 'Display version' );
    args = parser.parse_args ();
    
    ## Display version
    
    if ( args.version == True ):
        print ( __version__ );
        exit ( 0 );
    
    ## Valid required arguments
    
    if ( args.csv_file == None or os.path.isfile ( args.csv_file ) == False ):
        print ( 'Missing --csv-file file. -h to show help' );
        exit ( 2 );
    
    if ( args.dot_file != None ):
        """Dot file directory"""
        dot_file_dir = os.path.dirname ( args.dot_file );
        if ( os.path.isdir ( dot_file_dir ) == False ):
            print ( 'Wrong --dot-file value. Directory "{}" unexists'.format (
                dot_file_dir
            ) );
            exit ( 2 );
    
    ## Begin
    
    #
    # Init tool
    #
    
    """Csv > Dot"""
    csv_to_dot = CsvToDot (
        nodes_shape = args.nodes_shape,
        nodes_style = args.nodes_style,
        nodes_bg_color = args.nodes_bg_color,
        nodes_font_color = args.nodes_font_color
    );
    
    csv_to_dot.run (
        local_in_file = args.csv_file,
        delimiter = args.csv_delim,
        local_out_file = args.dot_file
    );
    
    exit ( 0 );

if __name__ == '__main__':
    run ();
