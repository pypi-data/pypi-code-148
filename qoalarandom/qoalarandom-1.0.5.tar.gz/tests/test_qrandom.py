from src.qrandom.qrandom import randint, randrange, randchoice

def test_randint():
    assert type(randint(0,2)) is int

def test_randrange():
    range_values = range(0,21,2)
    assert randrange(0,20,2) in range_values

def test_randchoice():
    food_choices = ['chicken','rice','pizza','ice cream', 'donuts']
    assert randchoice(food_choices) in food_choices