import os
import streamlit as st
import streamlit.components.v1 as components
import base64

WORD_CLOUD_IMAGE = ""
with open("wordcloud.jpg", "rb") as img_file:
    WORD_CLOUD_IMAGE = base64.b64encode(img_file.read())
#print(WORD_CLOUD_IMAGE)

_RELEASE = False

if _RELEASE:

    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _on_hover_tabs = components.declare_component(
        "st_on_machine_data",
        path = build_dir
    )

else:
    _on_hover_tabs = components.declare_component(
    "on_machine_data",
    url="http://localhost:3001"
    )

def on_machine_data(menu, group_names, text_groups,summaries,topics,generated_number_groups, word_cloud_image, default_choice=1, key=None):
    
    component_value = _on_hover_tabs(menu=menu, group_names=group_names, text_groups=text_groups,summaries=summaries,topics=topics,generated_number_groups=generated_number_groups, word_cloud_image=word_cloud_image, key=key)
    
    return component_value

if not _RELEASE:
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True) # Load the on hover side bar css file
    tabs = on_machine_data(menu=["World","Hello","Test"], 
                              group_names="Group Name", 
                              text_groups=['list 1','list 2','list 3','list 4'],
                              summaries="It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)",
                              topics='dffdsfsfsfsfsd',
                              generated_number_groups=10,
                              word_cloud_image=WORD_CLOUD_IMAGE,
                              key="1") ## create tabs for on hover navigation bar
    
    print(tabs)





        
