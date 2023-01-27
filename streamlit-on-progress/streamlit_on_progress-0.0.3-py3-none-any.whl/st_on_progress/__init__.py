import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if _RELEASE:

    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _on_hover_tabs = components.declare_component(
        "st_on_progress",
        path = build_dir
    )

else:
    _on_hover_tabs = components.declare_component(
    "on_progress",
    url="http://localhost:3001"
    )

def on_progress():
    
    component_value = _on_hover_tabs()
    
    return component_value

if not _RELEASE:
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True) # Load the on hover side bar css file


    tabs = on_progress() ## create tabs for on hover navigation bar

        
