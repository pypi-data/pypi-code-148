from cakework import Cakework

def say_hello(params):
    print("inside say_hello")
    return("hello " + params["name"])

cakework = Cakework(name="hello-world", local=False)
cakework.add_task(say_hello)
