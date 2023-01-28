from kerenor.states import StateM, Screen, start, BYE_TXT

try:
    import tkinter as tk
    has_tk_inter = True
except ModuleNotFoundError:
    has_tk_inter = False

root = None
canvas = None
bg_img = None


def user_input(num_options: int):
    userinput = -1
    while userinput < 0 or userinput > num_options-1:
        userinput = input("press number!\n")
        try:
            userinput = int(userinput)
        except:
            userinput = num_options + 1
    return userinput


def make_button(text: str, y_loc: int, canvas, next_option):
    double_line = text.find("\n")
    len_line = (len(text) if double_line < -1 else max(double_line, len(text) - double_line))
    button = tk.Button(root, text=text, command=next_option,
                       anchor='sw', width=len_line, background="#33B5E5", activebackground="#33C5DD")
    canvas.create_window(10, y_loc, anchor='nw', window=button)
    y_loc += 60 if double_line > 0 else 40
    return y_loc


def draw_wrapper(state: Screen):
    def draw_this_state():
        return draw_state_on_canvas(state)
    return draw_this_state


def draw_state_on_canvas(state: Screen):
    global root
    global canvas
    global bg_img
    if not canvas:
        canvas = tk.Canvas(root, width=520, height=520, bg='white')
    else:
        canvas.delete("all")
    text_note = tk.Label(canvas, text=state.text, font=state.font, wraplength=500, justify="left", bg='white')
    canvas.create_window(10, 20, window=text_note, anchor='nw')
    bg_img = tk.PhotoImage(file=state.bg_path)
    canvas.create_image(260, 260, image=bg_img)

    # buttons!
    y_loc = 470 - len(StateM[state]) * 50
    for ind, option in enumerate(StateM[state]):
        y_loc = make_button(text=option.text, canvas=canvas, y_loc=y_loc, next_option=draw_wrapper(option.next))
    make_button(text=BYE_TXT, canvas=canvas, y_loc=y_loc, next_option=root.quit)
    canvas.pack()


def run_tk():
    global root
    root = tk.Tk()
    root.title('KerenOr')
    draw_state_on_canvas(start)
    root.mainloop()


def eval_state(state: Screen):
    print(state.text)
    exit_ind = len(StateM[state]) + 1
    for option_ind, option in enumerate(StateM[state]):
        print(f"{option_ind + 1}.\t{option.text.replace('click here', 'select number')}")
    print(f"{exit_ind}.\t{BYE_TXT}")
    userinput = user_input(exit_ind + 1)
    if userinput == exit_ind:
        print("Bye!")
        exit(0)

    return StateM[state][userinput - 1].next


def run_cmd():
    current_state = start
    while True:
        current_state = eval_state(current_state)


def run_me():
    if has_tk_inter:
        run_tk()
    else:
        run_cmd()

