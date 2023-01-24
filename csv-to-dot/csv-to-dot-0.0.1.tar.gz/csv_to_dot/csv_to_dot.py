#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Convert .csv to .dot
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
import os;
import sys;
import jinja2;

from csv import reader;
from typing import Union;

from pprint import pprint;

#: Current module path
MODULE_PATH = os.path.dirname ( os.path.abspath ( __file__ ) );
#: Resource path
RESOURCE_PATH = os.path.join ( MODULE_PATH, 'resources' );


class CsvToDot:
    """Convert a 2 columns CSV file to a .dot, who can be converted with Graphviz to .jpg, .ps, ...
    
    Attributes:
        _csv_fh (handler): Protected. CSV file handler
        _node_indice (int): Protected. Indice to increment at each node
        _node_key_tpl (string): Protected. Template to create node key
        _nodes (dict): Protected. All nodes, key>label
        _edges (dict): Protected. Dict of list with all edges
        _dot_tpl (jinja2.Template): Protected. Jinja template for dot file
        _nodes_opts (dict): Protected. Nodes options
    """
    def __init__ ( self, nodes_shape: str = 'box', nodes_style: str = 'filled', nodes_bg_color: str = 'blue', nodes_font_color: str = 'white' ):
        """Default constructor
        
        Arguments:
            nodes_shape (str): Nodes option : shape, default : box
            nodes_style (str): Nodes option : style, default : filled
            nodes_bg_color (str): Nodes option : background color, default : blue
            nodes_font_color (str): Nodes option : font color, default : white
        """
        """CSV file handler"""
        self._csv_fh = None;
        
        """Indice to increment at each node"""
        self._node_indice = 0;
        
        """Template to create node key"""
        self._node_key_tpl = 'A{:03d}';
        
        """All node, key>label"""
        self._nodes = {};
        
        """Dict of list with all edges"""
        self._edges = {};
        
        """Jinja template for dot file"""
        self._dot_tpl = None;
        
        """Nodes options"""
        self._nodes_opts = {
            'shape': nodes_shape.strip (),
            'style': nodes_style.strip (),
            'bg_color': nodes_bg_color.strip (),
            'font_color': nodes_font_color.strip ()
        };
        
        self._init_resources ();
    
    
    def _init_resources ( self ):
        """Init resources used by system : init jinja2
        """
        ## Init jinja2
        self._init_j2 ();
    
    
    def _init_j2 ( self ):
        """Init jinja2
        """
        """Jinja2 environment"""
        env = jinja2.Environment (
            loader = jinja2.FileSystemLoader (
                RESOURCE_PATH
            )
        );
        
        self._dot_tpl = env.get_template (
            'graf.dot.j2'
        );
    
    
    def _dict_search_value ( self, d: dict, value: str ) -> Union[str,None]:
        """Search value on dict & returns key if exists
        
        Arguments:
            d (dict): Dictionnary to lookup
            value (string): Value to get key
        
        Returns:
            string|None: Key if found. None otherwise
        """
        try:
            return list ( d.keys () ) [ list ( d.values () ).index ( value ) ];
        except Exception as e:
            ## Value not found
            pass;
        return None;
    
    
    def _nodes_search_value ( self, value: str ) -> Union[str,None]:
        """Seach node key from value
        
        Arguments:
            value (string): Node value to get key
        
        Returns:
            string|None: Node key if found. None otherwise
        """
        return self._dict_search_value (
            d = self._nodes,
            value = value
        );
    
    
    def _create_node_key ( self ) -> str:
        """Create new node key
        
        Returns:
            string: Node key
        """
        ## Increment indice
        self._node_indice += 1;
        return self._node_key_tpl.format (
            self._node_indice
        );
    
    
    def _get_node_key ( self, node: str ) -> str:
        """Get/create a node key
        
        Arguments:
           node (string): Node label
        
        Returns:
           string: Key associated to label
        """
        """Key associated to label"""
        ret = self._nodes_search_value (
            value = node
        );
        
        if ( ret != None ):
            ## Key already exists
            return ret;
        
        ## Create new key & store node
        ret = self._create_node_key ();
        self._nodes [ ret ] = node;
        return ret;
    
    
    def _add_edge ( self, n1: str, n2: str ):
        """Store edge between n1 > n2
        
        Arguments:
            n1 (string): Node 1 : label
            n2 (string): Node 2 : label
        """
        """Node 1 : key"""
        key_n1 = self._get_node_key ( node = n1 );
        """Node 2 : key"""
        key_n2 = self._get_node_key ( node = n2 );
        
        if ( key_n1 not in self._edges ):
            self._edges [ key_n1 ] = [];
        
        self._edges [ key_n1 ].append ( key_n2 );
    
    
    def _get_fh_csv ( self, local_file: str ):
        """Open file handler : csv file (singleton)
        
        Arguments:
            local_file (string): Absolute local file path to csv file
        
        Returns:
            handler: Opened file
        """
        if ( self._csv_fh == None ):
            self._csv_fh = open ( local_file, 'r' );
        return self._csv_fh;
    
    
    def _close_fh ( self ):
        """Close file handlers
        """
        try:
            ## Close : csv file
            self._csv_fh.close ();
            self._csv_fh = None;
        except Exception as e:
            pass;
    
    
    def _csv_reader ( self, local_file: str, delimiter: str ):
        """Create CSV reader
        
        Arguments:
            local_file (string): Absolute local file path to csv file
            delimiter (string): Csv delimiter
        
        Returns:
            csv.Reader: Csv reader
        """
        return reader (
            self._get_fh_csv (
                local_file = local_file
            ),
            delimiter = delimiter
        );
    
    
    def _flat_edges_to_dot ( self ) -> list:
        """Convert all edges to a list for templating
        
        Returns:
            string[]: Edges for jinja2 templates
        """
        """Edges"""
        ret = [];
        
        for n1 in self._edges:
            for n2 in self._edges [ n1 ]:
                ret.append (
                    '{n1} -> {n2};'.format (
                        n1 = n1,
                        n2 = n2
                    )
                );
        
        return ret;
    
    
    def _flat_nodes_to_dot ( self ) -> list:
        """Convert all nodes to a list for templating
        
        Returns:
            string[]: Nodes for jinja2 templates
        """
        """Nodes"""
        ret = [];
        
        for key in self._nodes:
            ret.append (
                '{key} [label="{node}"];'.format (
                    key = key,
                    node = self._nodes [ key ]
                )
            );
        
        return ret;
    
    
    def _print_dot_stdout ( self, content: str ):
        """Print dot file on stdout
        
        Arguments:
            content (string): Content to print
        """
        sys.stdout.write ( content );
    
    
    def _print_graphvz_instructions ( self, local_file: str ):
        """Print some instructions to use graphwiz on stdout
        
        Arguments:
            local_file (string): Absolute local file path to create .dot file
        """
        """Destination file name"""
        dest_file = local_file.split ( '.' );
        if ( len ( dest_file ) > 1 ):
            dest_file.pop ();
        dest_file.append ( '<EXT>' );
        
        sys.stdout.write (
            "Dot file created at : {local_file}\nRun command :\n  dot -T<EXT> {local_file} -o {dest_file} # Replace <EXT> with required format\nNB : Require debian package : `graphviz`\n".format (
                local_file = local_file,
                dest_file = '.'.join ( dest_file )
            )
        );
    
    
    def _print_dot_file ( self, local_file: str, content: str ):
        """Print dot file on stdout
        
        Arguments:
            local_file (string): Absolute local file path to create .dot file
            content (string): Content to print
        """
        with open ( local_file, 'w' ) as fh:
            fh.write ( content );
        
        self._print_graphvz_instructions (
            local_file = local_file
        );
    
    
    def _print_dot ( self, local_file: Union[str,None] = None ) -> bool:
        """Print dot file
        
        Arguments:
            local_file (string|None): Absolute local file path to create .dot file. If None, print on stdout
        
        Returns:
            bool: True if write on stdout. False otherwise
        """
        """Dot file content"""
        content = self._dot_tpl.render (
            edges = self._flat_edges_to_dot (),
            nodes = self._flat_nodes_to_dot (),
            nodes_opts = self._nodes_opts
        );
        content = "{}\n".format ( content );
        
        if ( local_file == None ):
            self._print_dot_stdout (
                content = content
            );
            return True;
        
        self._print_dot_file (
            local_file = local_file,
            content = content
        );
        return False;
    
    
    def run ( self, local_in_file: str, delimiter: str = ';', local_out_file: Union[str,None] = None ):
        """Run process csv > dot
        
        Arguments:
            local_in_file (string): Absolute local file path to csv file
            delimiter (string): Csv delimiter. Default : ';'
            local_out_file (string|None): Absolute local file path to create .dot file. If None, print on stdout
        """
        ## Process .csv
        
        """CSV reader"""
        r_csv = self._csv_reader (
            local_file = local_in_file,
            delimiter = delimiter
        );
        
        for row in r_csv:
            self._add_edge (
                n1 = row [ 0 ],
                n2 = row [ 1 ]
            );
        
        self._close_fh ();
        
        ## Process : .dot
        
        self._print_dot (
            local_file = local_out_file
        );
