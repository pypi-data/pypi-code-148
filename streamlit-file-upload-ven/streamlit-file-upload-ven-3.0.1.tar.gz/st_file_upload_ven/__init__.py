import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_file_upload_ven",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_file_upload_ven", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
# def my_component(name, key=None):
def file_upload_ven(menu,group_names,text_groups,summaries,topics,generated_number_groups, isUploaded, key=None):
    component_value = _component_func(menu=menu,group_names=group_names,text_groups=text_groups,summaries=summaries,topics=topics,generated_number_groups=generated_number_groups, isUploaded=isUploaded, key=key, default=0)
    print("component_value")
    print(component_value)
    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    # st.subheader("Component with constant args")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True) # Load the on hover side bar css file

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    #uploaded_file = file_upload_ven(menu=["World","Hello","Test"],group_names=["World","Hello","Test"],text_groups=[],summaries="dfdffdfddfsfsdfsfsfssd",topics='dffdsfsfsfsfsd',generated_number_groups=7, False)
    uploaded_file = file_upload_ven(["World","Hello","Test"],"Group Name",['list 1','list 2','list 3','list 4'],"It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)",'dffdsfsfsfsfsd',10, False)
    
    if uploaded_file is not None:
        # To read file as bytes:
        #bytes_data = uploaded_file.getvalue()
        #uploaded_file = my_component("World", DATA[0])
        st.write(uploaded_file)

        # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        # dataframe = pd.read_csv(uploaded_file)
        # st.write(dataframe)
    #my_component()
    # st.markdown("You've clicked %s times!" % int(num_clicks))

    # st.markdown("---")
    # st.subheader("Component with variable args")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    # name_input = st.text_input("Enter a name", value="Streamlit")
    # num_clicks = my_component(name_input, key="foo")
    # st.markdown("You've clicked %s times!" % int(num_clicks))
