from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images
import sys
import pyfiglet

def show(screen, img, frames, time, effect_type, background, transparent):
    
    # CREATE THE RENDERER
    renderer = FocusRenderer(screen, frames, time, img, effect_type, background, transparent, start_frame=100)

    # SET EFFECT ATTRIBUTES
    renderer.effect.update_color_properties(color=True, characters=True, random_color=True)
    renderer.effect.update_grey_scale_size(10)

    # RUN THE ANIMATION
    renderer.run(end_message=True)

    # CATCH THE END WITH INPUT() --> for Win-Systems --> Ctl-C for Unix-Systems
    input()


def main():
    image = images.text_to_image("Hello from bruhanimate!", padding_top_bottom=1, padding_left_right=3)
    Screen.show(show, args=(image, 300, 0, "plasma", " ", False))


if __name__ == "__main__":
    main()