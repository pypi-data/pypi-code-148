from engine import element, event, image, window
import clipboard
import pygame

class _TextHolder(element.Element):
    def __init__(self, name:str, elements:element.Elements, x:int, y:int, placeholder:str="Typing Here", max_chars:int=None, is_password:bool=False, onchange=None) -> None:
        self.set_font()
        super().__init__(name, elements, image.Text(placeholder, self.font, (224, 224, 224), self.size, self.bold, self.italic), x, y)
        self.text = ""
        self.placeholder = placeholder
        self.is_password = is_password
        self.onchange = onchange
        self.max_chars = max_chars
        self.is_focus = False
        self.__typed = 0

        self.all_chars = {
            pygame.K_a: lambda:self.text + 'a',
            pygame.K_b: lambda:self.text + 'b',
            pygame.K_c: lambda:self.text + 'c',
            pygame.K_d: lambda:self.text + 'd',
            pygame.K_e: lambda:self.text + 'e',
            pygame.K_f: lambda:self.text + 'f', 
            pygame.K_g: lambda:self.text + 'g',
            pygame.K_h: lambda:self.text + 'h',
            pygame.K_i: lambda:self.text + 'i',
            pygame.K_j: lambda:self.text + 'j',
            pygame.K_k: lambda:self.text + 'k',
            pygame.K_l: lambda:self.text + 'l',
            pygame.K_m: lambda:self.text + 'm',
            pygame.K_n: lambda:self.text + 'n',
            pygame.K_o: lambda:self.text + 'o',
            pygame.K_p: lambda:self.text + 'p',
            pygame.K_q: lambda:self.text + 'q',
            pygame.K_r: lambda:self.text + 'r',
            pygame.K_s: lambda:self.text + 's',
            pygame.K_t: lambda:self.text + 't',
            pygame.K_u: lambda:self.text + 'u',
            pygame.K_v: lambda:self.text + 'v',
            pygame.K_w: lambda:self.text + 'w',
            pygame.K_x: lambda:self.text + 'x',
            pygame.K_y: lambda:self.text + 'y',
            pygame.K_z: lambda:self.text + 'z',
            pygame.K_0: lambda:self.text + '0',
            pygame.K_1: lambda:self.text + '1',
            pygame.K_2: lambda:self.text + '2',
            pygame.K_3: lambda:self.text + '3',
            pygame.K_4: lambda:self.text + '4',
            pygame.K_5: lambda:self.text + '5',
            pygame.K_6: lambda:self.text + '6',
            pygame.K_7: lambda:self.text + '7',
            pygame.K_8: lambda:self.text + '8',
            pygame.K_9: lambda:self.text + '9',
            pygame.K_SPACE: lambda:self.text + ' ',
            pygame.K_BACKSPACE: lambda:self.text[:-1]
        }

    def set_font(self, font:str="arial", color:tuple[int, int, int]=(0, 0, 0), size:int=32, bold:bool=False, italic:bool=False):
        self.font = font
        self.color = color
        self.size = size
        self.bold = bold
        self.italic = italic

        if hasattr(self, "text"):
            self.update_text(self.text)

    def add_char(self, key, func):
        self.all_chars.update({key: func})

    def update_text(self, text:str):
        if text and not self.is_password:
            self.ori_image = image.Text(text, self.font, self.color, self.size, self.bold, self.italic).get_surface()
        elif text and self.is_password:
            self.ori_image = image.Text('*' * len(text), self.font, self.color, self.size, self.bold, self.italic).get_surface()
        else:
            self.ori_image = image.Text(self.placeholder, self.font, (224, 224, 224), self.size, self.bold, self.italic).get_surface()

        self.image = self.ori_image
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def get_text(self):
        return self.text

    def update(self, window:window.Window) -> None:
        if self.is_clicked(0):
            self.is_focus = True

        if self.is_focus:
            for idx, char in enumerate(self.all_chars):
                if self.is_key_pressed(char):
                    if self.__typed <= 0:
                        if (self.max_chars and (len(self.text) < self.max_chars) or (len(self.all_chars[char]()) <= self.max_chars)) or not self.max_chars:
                            if not (self.is_key_pressed(pygame.K_LCTRL) or self.is_key_pressed(pygame.K_RCTRL)):
                                if idx < 26 and (self.is_key_pressed(pygame.K_LSHIFT) or self.is_key_pressed(pygame.K_RSHIFT)):
                                    self.text += self.all_chars[char]()[-1].upper()
                                else:
                                    self.text = self.all_chars[char]()

                            if (self.is_key_pressed(pygame.K_LCTRL) or self.is_key_pressed(pygame.K_RCTRL)) and self.is_key_pressed(pygame.K_v):
                                clip = clipboard.paste()
                                for char in clip:
                                    if (self.max_chars and (len(self.text) < self.max_chars)) or not self.max_chars:
                                        self.text += char

                            if self.onchange:
                                self.onchange(self.text)

                            self.__typed = 150
                
                    self.update_text(self.text)

                else:
                    self.__typed -= 1

            if self.is_key_pressed(pygame.K_ESCAPE):
                self.is_focus = False

class TextEdit:
    def __init__(self, name:str, group:str, window:window.Window, elements:element.Elements, x:int, y:int, placeholder:str="Typing Here", max_chars:int=None, is_password:bool=False, onchange=None) -> None:
        self.onchange_event = onchange
        self.text_holder = _TextHolder(name, elements, x, y, placeholder, max_chars, is_password, self.onchange_event)
        elements.add_element(name, group, self.text_holder)

    def onchange(self, text:str):
        if self.onchange_event:
            self.onchange_event(text)