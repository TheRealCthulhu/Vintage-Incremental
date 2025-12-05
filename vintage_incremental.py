"""
Cameron Lanphere
Asa Rousseau
Final Project - Vintage Incremental
"""


# Imports
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from functools import partial
from gamevars import *
import simpleaudio as sa
import threading as th


# region Function Definitions


def exit_game():
    root.destroy()


def create_thread(tgt):
    th.Thread(target=tgt).start()


def create_resource_button(parent, txt, bg_color, img=None, height=60, width=250, compound=None, fnt=(def_font, 18, "bold"), cmd=exit_game, img_scale=2, **kwargs):
    if img:
        if img_scale != 1:
            image = Image.open(img)
            new_wid = image.width * 2
            new_hei = image.height * 2
            re_img = image.resize((new_wid, new_hei), Image.Resampling.LANCZOS)
            tmp_icon = ImageTk.PhotoImage(re_img)
        else:
            tmp_icon = tk.PhotoImage(file=img)
        tmp_btn = tk.Button(parent, image=tmp_icon, font=fnt, text=txt, compound=compound,
                            command=cmd, bg=bg_color, height=height, width=width, **kwargs)
        tmp_btn.image = tmp_icon
    else:
        tmp_btn = tk.Button(parent, font=fnt, text=txt,
                            bg=bg_color, image=PXL_SIZER,
                            compound='c', height=height, width=width, command=cmd, **kwargs)
    return tmp_btn


def create_resource_label(parent, variable, bg_color, height=60, fnt=(def_font, 18, "bold")):
    temp_lbl = tk.Label(parent, textvariable=variable, image=PXL_SIZER,
                        compound='c', bg=bg_color, height=height, font=fnt, padx=5)
    return temp_lbl


def start_game():
    main = tk.Toplevel(root, background="springgreen4")
    play_sound(START_SOUND)
    main.attributes("-fullscreen", True)
    stick_btn = create_resource_button(main, "Scrounge for Sticks   ",
                                       "saddlebrown", STICK_ICON, compound="right", cmd=partial(create_thread, gather_stick), activebackground="#753a10")
    stick_lbl = create_resource_label(main, sticks, "saddlebrown")
    stick_btn.place(x=50, y=50)
    stick_lbl.place(x=310, y=50)
    stone_btn = create_resource_button(main, "Scrounge for Stones   ", "slate gray", STONES_ICON,
                                       compound="right", cmd=partial(create_thread, gather_stone), activebackground="dim gray")
    stone_lbl = create_resource_label(main, stones, "slate gray")
    stone_btn.place(x=50, y=140)
    stone_lbl.place(x=310, y=140)
    opt_icon = tk.PhotoImage(file=SETTINGS_GEAR)
    opt_btn = tk.Button(main, image=opt_icon,
                        command=partial(opt_menu, main), bg="springgreen4",
                        bd=0, fg="red", activebackground="springgreen4")

    opt_btn.image = opt_icon

    opt_btn.pack(side="top", anchor="ne", padx=10, pady=10)
    root.withdraw()


def gather_stick():
    if gather_tool == None:
        time.sleep(1)
        sticks.set(sticks.get() + 1)
    root.update_idletasks()


def gather_stone():
    if gather_tool == None:
        time.sleep(1)
        stones.set(stones.get() + 1)
    root.update_idletasks()


def play_sound(file, wait=False):
    sound = sa.WaveObject.from_wave_file(file)
    player = sound.play()
    if wait == True:
        player.wait_done()


def cntr_wnd(wnd):
    x = ((screen_width // 2) - (wnd.winfo_reqwidth() // 2))
    y = ((screen_height // 2) - (wnd.winfo_reqheight() // 2))
    wnd.geometry(f"{wnd.winfo_reqwidth()}x{wnd.winfo_reqheight()}+{x}+{y}")


def dstr_wnd(wnd, p_wnd=None, pnoise=True):
    if pnoise == True:
        play_sound(NEG_MENU)
    if p_wnd:
        p_wnd.focus_force()
    wnd.destroy()


def return_to_mm(wind, cscrn):
    root.deiconify()
    dstr_wnd(wind)
    dstr_wnd(cscrn, pnoise=False)


def reset_vars():
    for v in resource_vars:
        v.set(0)


def opt_menu(pw):
    prev_wnd = pw
    options = tk.Toplevel(root, bg="chartreuse4", bd=20.0, relief="raised")
    options.withdraw()
    play_sound(POS_MENU)
    options.configure(width=WND_TALL[0], height=WND_TALL[1])
    options.grab_set()
    options.resizable(False, False)
    options.update_idletasks()
    options.overrideredirect(True)
    cntr_wnd(options)
    if root.winfo_ismapped() == False:
        bk_btn = tk.Button(options, font=(def_font, 24, "bold"), text="X", image=PXL_SIZER, compound='c', background="dark olive green", activebackground="dark green", foreground="firebrick4",
                           command=partial(dstr_wnd, options, prev_wnd), padx=10, height=20, relief="ridge", bd=1).pack(side="top", anchor="ne")
        opt_ttl = tk.Label(options, text="Options", font=(
            def_font, 60, "bold"), background="chartreuse4").pack(side="top")
        mm_btn = tk.Button(options, font=(def_font, 24, "bold"), text="Main Menu", image=PXL_SIZER, compound='c', height=35, background="red3", activebackground="red4", padx=15, command=partial(
            return_to_mm, options, prev_wnd)).pack(side="bottom", pady=15)
    elif root.winfo_ismapped() == True:
        bk_btn = tk.Button(options, text="Back", background="firebrick3",
                           command=partial(dstr_wnd, options, prev_wnd),
                           padx=10, pady=10, relief="ridge", bd=1
                           ).pack(side="bottom", pady=40)
        opt_ttl = tk.Label(options, text="Options", font=(
            def_font, 60, "bold"), background="chartreuse4").pack(side="top")
    options.deiconify()

# endregion Function Definitions


if __name__ == "__main__":
    root = tk.Tk()
    # region create resource vars
    sticks = tk.IntVar()
    sticks.set(0)
    resource_vars.append(sticks)
    stones = tk.IntVar()
    stones.set(0)
    resource_vars.append(stones)
    # endregion
    PXL_SIZER = tk.PhotoImage(width=1, height=1)
    root.attributes("-fullscreen", True)
    root.configure(background=bgc)

    # region Main Menu
    ttl = tk.Label(root, text="Vintage Incremental", font=(def_font, 60, "bold"),
                   background=bgc).pack(side="top")
    exit_btn = tk.Button(root, text="Quit", font=(
        def_font, 24), command=exit_game, padx=50, background="firebrick3", activebackground="firebrick4",
        relief="ridge", bd=5).pack(side="bottom", pady=15)
    strt_btn = tk.Button(root, text="New Game", font=(
        def_font, 24), command=start_game, background="olive drab", activebackground="forestgreen",
        padx=80).pack(side="top", pady=120)
    ctn_btn = tk.Button(root, text="Continue", font=(
        def_font, 24), command=exit_game, background="snow4", activebackground="grey36",
        padx=80).pack(side="top")
    opt_btn = tk.Button(root, text="Options", font=(
        def_font, 24), command=partial(opt_menu, root), background="mediumorchid3", activebackground="mediumorchid4",
        padx=80).pack(side="top", pady=40)

    # endregion Main Menu

    root.mainloop()
