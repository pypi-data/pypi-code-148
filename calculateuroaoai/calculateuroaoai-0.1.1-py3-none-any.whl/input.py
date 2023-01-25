import config

def test_config_file():
    print(f"Hello {config.my_name} !!")

def test_2_config_file():
    with(open('config.py','r')) as config_file:
        print(f"Hello {config_file.my_name} !!")