import random
import click
from gamepkg.utils.utils import win_logic


@click.command()
@click.option('--usr', type=click.Choice(["R", "P", "S"],
                                         case_sensitive=False), required=True,
              help="Choose R for  rock, P for paper and S for scissor !",
              prompt="Choose R for  rock, P for paper and S for scissor !")
def game(usr):
    usr = usr.upper()
    cmp = random.choice(['R', 'P', 'S'])
    if usr not in ['R', 'P', 'S']:
        return 'Wrong choice'

    if usr == cmp:
        print('TIE')
        return 'TIE'

    if win_logic(usr, cmp):
        print('User win')
        return 'User win'
    print('Computer win')
    return 'Computer win'


if __name__ == "__main__":
    result = game()
