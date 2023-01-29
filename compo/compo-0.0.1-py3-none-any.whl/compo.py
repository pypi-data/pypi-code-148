from pydantic import BaseModel


class Compo(BaseModel):
    pass


class Profile(Compo):
    name: str
        

class Skill(Compo):
    skill_title: list[str]
    profile: Profile
    

skill = Skill(profile=Profile(name="labas"), skill_title=["vienas", "du"])


skill2 = Skill.parse_obj({'skill_title': ['vienas', 'du', "trys"], 'profile': {'name': 'namas'}})
breakpoint()
pass


## Lets create a Pydantic class.



## This should be Python package.


## Latest consideration: should JSON be typed using Pydantic.
# Lets create a single served page, which would have Pydantic installed.
# A way to print the state.
# Component: Each Pydantic type should have a place to attach and its template.
# Pydantic should be able to output as JSON.



# ## Consider writing a plugin for an app:
# # https://docs.pyscript.net/unstable/guides/custom-plugins.html
# ## Consider writing a virtual DOM library:
# # https://dev.to/ycmjason/building-a-simple-virtual-dom-from-scratch-3d05
# # https://medium.com/@deathmood/how-to-write-your-own-virtual-dom-ee74acc13060


# class Element:
#     innerHtml = "<div>{ name } and { surname }</div>"

#     def __init__(self, name):
#         pass

#     def write(self, value, append=False):
#         print(value)
#         return value


# # How to handle 

# # GET_LIST
# # GET
# # POST
# # PUT
# # DELETE

# # Pagination.

# # Rerendering.
#     # Template could be written as jinja tempalte, which would be initailly loaded and than updated on changes.

# # Whole tree has to be rendered.
#     # Template in Jinja?


# class dom_dict(dict):

#     # id is added on initialization
#     def __init__(self, template_id: str):
#         pass


# class dom_list(list):
#     """
#     Works like a simple list, except each element is rendered to template and stored in the container.
#     Also an API call can be made.
#     """

#     def __init__(self, container_id: str, template_id: str, url: str, jwt_token: str, *args, **kwargs):
#         self.container_id = container_id
#         self.template_id = template_id
#         result = super().__init__(*args, **kwargs)
#         return result

#     def _render(self, values: dict):
#         # Renders values into an element
#         return Element(self.template_id).innerHtml.format(values)

#     def append(self, value) -> None:
#         result = super().append(value)
#         Element(self.container_id).write(self._render(value), append=True)
#         return result

#     def insert(self, index, value) -> None:
#         result = super().insert(index, value)
#         return result

#     def pop(self, index: int, **kwargs):
#         result = super().pop(index, **kwargs)
#         return result

#     def remove(self, value) -> None:
#         result = super().remove(value)
#         return result


# my_list = dom_list("container-id", "template-id")
# my_list.append({"name": "hello-world", })

