import real_json
import json


def test_get_wrapped_json():

    data = {
        "a": 1,
        "b": 2,
        "c": {
            "d": 3,
            "e": 4,
        },
        "f": [5, 6, 7],
    }
    wrapped = real_json.ify(data)

    # Test attribute access
    assert wrapped.a == 1
    assert wrapped.b == 2
    assert wrapped.c.d == 3
    assert wrapped.c.e == 4
    assert wrapped.f[0] == 5
    assert wrapped.f[1] == 6
    assert wrapped.f[2] == 7
    assert wrapped.f[3] == None
    assert wrapped.g == None
    assert wrapped.c.f == None

    # Test item access
    assert wrapped["a"] == 1
    assert wrapped["b"] == 2
    assert wrapped["c"]["d"] == 3
    assert wrapped["c"]["e"] == 4
    assert wrapped["f"][0] == 5
    assert wrapped["f"][1] == 6
    assert wrapped["f"][2] == 7
    assert wrapped["g"] == None
    assert wrapped["c"]["f"] == None

    # Test set attribute
    wrapped.a = 10
    assert wrapped.a == 10
    wrapped.g = 20
    assert wrapped.g == 20

    # Test set item
    wrapped["b"] = 20
    assert wrapped["b"] == 20
    wrapped["h"] = 30
    assert wrapped["h"] == 30

    # Test str and repr
    assert str(wrapped) == str(data)
    assert repr(wrapped) == repr(data)

    # Test len
    print("wrapped:", wrapped)
    assert len(wrapped) == 6
    assert len(wrapped.c) == 2
    assert len(wrapped.f) == 3

    # Test bool
    assert bool(wrapped) == True
    assert bool(wrapped.g) == True
    assert bool(wrapped.c) == True
    assert bool(wrapped.f)

    json.dump(wrapped.__dict__["_data"], "wrapped.json")

    data = {
        "name": "John",
        "age": 30,
        "cars": [
            {"model": "Ford", "year": 2020},
            {"model": "BMW", "year": 2019}
        ]
    }

    wrapped_data = real_json.ify(data)

    # Accessing values using dot notation
    print(wrapped_data.name)  # Output: "John"
    print(wrapped_data.age)  # Output: 30
    # Output: [{"model": "Ford", "year": 2020}, {"model": "BMW", "year": 2019}]
    print(wrapped_data.cars)

    # Accessing values using square brackets notation
    print(wrapped_data['name'])  # Output: "John"
    print(wrapped_data['age'])  # Output: 30
    # Output: [{"model": "Ford", "year": 2020}, {"model": "BMW", "year": 2019}]
    print(wrapped_data['cars'])

    # Accessing values that are not present in the data
    print(wrapped_data.address)  # Output: None
    print(wrapped_data['address'])  # Output: None

    # Accessing elements of the list using index notation
    print(wrapped_data.cars[0])  # Output: {"model": "Ford", "year": 2020}
    print(wrapped_data['cars'][0])  # Output: {"model": "Ford", "year": 2020}

    # Accessing elements of the list using index notation
    print(wrapped_data.cars[0].model)  # Output: "Ford"
    print(wrapped_data['cars'][0]['model'])  # Output: "Ford"

    # Accessing elements of the list using index notation
    print(wrapped_data.cars[2])  # Output: None
    print(wrapped_data['cars'][2])  # Output: None

    # Accessing elements of the list using index notation
    print(wrapped_data.cars[0].color)  # Output: None
    print(wrapped_data['cars'][0]['color'])  # Output: None

    json.dump(wrapped_data.__dict__["_data"], "data.json")


test_get_wrapped_json()
