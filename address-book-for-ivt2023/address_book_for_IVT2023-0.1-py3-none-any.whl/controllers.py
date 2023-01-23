from views import render_template
from models import User, Phone, Address


def default_controller(data=None, cls=True):
    """Default controller"""
    render_template(context={}, template="default.jinja2", cls=cls)
    return input(), None


def exit_controller(data=None, cls=True):
    render_template(context={}, template="exit.jinja2", cls=cls)
    exit()


def all_users_controller(data=None, cls=True):
    users = User.all()
    render_template(context={'users': users}, template="all_users.jinja2", cls=cls)
    input("Продолжить?")
    return 'main', None  # (next state, data)


def add_user_controller(data=None, cls=True):
    render_template(context={}, template="add_user.jinja2", cls=cls)
    username = input()
    user = User.add(username)
    return 21, user  # (next state, data)


def add_phone_controller(user, cls=True):
    render_template(context={}, template="add_phone.jinja2", cls=cls)
    phone_number = input()
    phone = Phone.add(phone_number, user)
    return 212, user  # (next state, data)


def add_address_controller(user, cls=True):
    render_template(context={}, template="add_address.jinja2", cls=cls)
    address_number = input()
    address = Address.add(address_number, user)
    return 222, user  # (next state, data)


def add_more_controller(user, cls=True):
    render_template(context={}, template="add_more1.jinja2", cls=cls)
    answer = input()
    if answer == 'Y':
        return 21, user
    return 22, user  # (next state, data)


def add_more_address_controller(user, cls=True):
    render_template(context={}, template="add_address.jinja2", cls=cls)
    answer = input()
    if answer == 'Y':
        return 22, user
    return 51, user  # (next state, data)


def get_controller(state):
    return controllers_dict.get(state, default_controller)


controllers_dict = {  # use dict type instead of if else chain
    '0': exit_controller,
    '1': all_users_controller,
    '2': add_user_controller,
    21: add_phone_controller,  # user can't enter 21 of int type
    212: add_more_controller,
    22: add_address_controller,
    222: add_more_address_controller,
}
