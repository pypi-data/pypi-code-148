import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if _RELEASE:

    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _on_hover_tabs = components.declare_component(
        "st_top_menu",
        path = build_dir
    )

else:
    _on_hover_tabs = components.declare_component(
    "on_top_menu",
    url="http://localhost:3001"
    )

def on_top_menu(embed, temp, similar):
    
    component_value = _on_hover_tabs(embed=embed, temp=temp, similar=similar)
    
    return component_value

if not _RELEASE:
 

         tabs = on_top_menu(embed=['Dashboard', 'Money', 'Economy'], 
                              temp=['dashboard', 'money', 'economy'], 
                              similar=['dashboard', 'money', 'economy'],) ## create tabs for on hover navigation bar
