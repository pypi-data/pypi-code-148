from cakework import Cakework

def say_hello(name):
    print("inside say_hello")
    return("hello " + name)

cakework = Cakework(name="myproj", local=True)
cakework.add_task(say_hello)
