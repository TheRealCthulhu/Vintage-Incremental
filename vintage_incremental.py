"""
Cameron Lanphere
Asa Rousseau
Final Project - Vintage Incremental
"""


# Imports
import sys
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from functools import partial
import gamevars as gv
import simpleaudio as sa
import threading as th


# region Function Definitions


def exit_game():
    root.destroy()


def create_thread(tgt, dm=False):
    th.Thread(target=tgt, daemon=dm).start()


def create_resource_button(parent, txt, bg_color, img=None, height=60, width=250, compound=None, fnt=(gv.def_font, 18, "bold"), cmd=exit_game, img_scale=2, **kwargs):
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


def create_resource_label(parent, variable, bg_color, height=60, fnt=(gv.def_font, 18, "bold")):
    temp_lbl = tk.Label(parent, textvariable=variable, image=PXL_SIZER,
                        compound='c', bg=bg_color, height=height, font=fnt, padx=5)
    return temp_lbl


def upd(pg, tm, btn, cmd=None, smh=True):
    btn["state"] = "disabled"
    pg
    # print("PG TEST START")
    pg["maximum"] = 1000
    # print(smh)
    if smh == False:
        for i in range(0, 1000, (100//tm)):
            pg["value"] = i
            # print(pg["value"])
            root.after(100, pg.update())
    elif smh == True:
        # print(tm)
        for i in range(0, 1000, (10//tm)):
            pg["value"] = i
            # print(pg["value"])
            root.after(10, pg.update())
    if cmd:
        cmd()
    btn["state"] = "normal"
    pg["value"] = 0


def create_resource_pg_bar(pt, max=100, style_name="Horizontal.TProgressbar"):
    temp_bar = ttk.Progressbar(pt,
                               value=0, maximum=max, orient="horizontal", style=style_name, length=257)
    return temp_bar


def stone_knapping(p_wnd=None):
    if stones.get() >= 2:
        stones.set(stones.get() - 1)
        rec = tk.StringVar(value="Nothing")
        sk = tk.Toplevel(p_wnd, background="saddlebrown")
        sk.configure(width=gv.WND_SQUARE, height=gv.WND_SQUARE)
        sk.focus_force()
        sk.grab_set()
        sk.resizable(False, False)
        cntr_wnd(sk)
        sk.overrideredirect(True)
        global stone_tiles
        stone_tiles = [[], [], [], [], []]
        confirm_btn = tk.Button(
            sk, text="Craft", width=15, height=2, command=None)
        confirm_btn.configure(command=partial(
            craft_knapped_item, True, sk, p_wnd))
        xp = 60
        yp = 25
        for i in range(5):
            for c in range(5):
                temp_bool = tk.BooleanVar()
                stone_tiles[i].append(temp_bool)
                temp_tile = tk.Checkbutton(
                    sk, variable=stone_tiles[i][c], width=70, height=70, indicatoron=False, image=PXL_SIZER, onvalue=1, offvalue=0, compound='c', bg="slate gray", selectcolor="dim gray", command=partial(create_thread, partial(check_sk_recipe, stone_tiles, rec), True))
                temp_tile.configure(command=partial(create_thread, partial(
                    check_sk_recipe, stone_tiles, rec, temp_tile, confirm_btn), True))
                temp_tile.place(x=xp, y=yp)
                xp += 70
            yp += 70
            xp -= (350)
        knap_lbl = tk.Label(sk, textvariable=rec, width=20)
        knap_lbl.place(x=gv.WND_SQUARE//2 - 70, y=430)
        cancel_btn = tk.Button(
            sk, text="Cancel", command=partial(dstr_wnd, sk, p_wnd), width=15, height=2)
        cancel_btn.place(x=15, y=430)
        confirm_btn.place(x=gv.WND_SQUARE - 125, y=430)


def craft_knapped_item(called_from_button=False, wnd=None, p_wnd=None):
    valid_recipe = check_sk_recipe(stone_tiles)
    if called_from_button:
        if valid_recipe == "1x Stone Blade":
            stone_blades.set(stone_blades.get() + 1)
            dstr_wnd(wnd, p_wnd)
        elif valid_recipe == "2x Stone Blade":
            stone_blades.set(stone_blades.get() + 2)
            dstr_wnd(wnd, p_wnd)
        stone_blades_str.set(f"Stone Blades: {stone_blades.get()}")


def check_sk_recipe(ary, tvar=None, btn=None, c_btn=None):
    if btn:
        btn["state"] = "disabled"
    if c_btn:
        c_btn["state"] = "disabled"
    tmp = [[], [], [], [], []]
    r = 0
    for i in ary:
        for c in i:
            tmp[r].append(not c.get())
        r += 1
    r = 0
    for recipe in gv.RECIPES:
        if tmp == gv.RECIPES[recipe][0]:
            if tvar:
                tvar.set(gv.RECIPES[recipe][1])
            if c_btn:
                c_btn["state"] = "normal"
            return (gv.RECIPES[recipe][1])
        else:
            if tvar:
                tvar.set("Nothing")


def start_game(res=False):
    gv.mm_vis = False
    if res == True:
        reset_vars()
    gv.has_save = True
    main = tk.Toplevel(root, background="springgreen4")
    main.withdraw()
    play_sound(gv.START_SOUND)
    main.attributes("-fullscreen", True)
    stick_bar = create_resource_pg_bar(
        pt=main, max=100, style_name="stick.Horizontal.TProgressbar")
    stone_bar = create_resource_pg_bar(
        main, 100, "stone.Horizontal.TProgressbar")
    stick_btn = create_resource_button(main, "Scrounge for Sticks   ",
                                       "saddlebrown", gv.STICK_ICON, compound="right", cmd=None, activebackground="#753a10", foreground="gray1")
    stick_btn.configure(command=partial(
        create_thread, (partial(upd, stick_bar, 1, stick_btn, gather_stick, True))))
    stick_lbl = create_resource_label(main, sticks, "saddlebrown")
    stick_btn.place(x=50, y=50)
    stick_lbl.place(x=310, y=50)
    stone_btn = create_resource_button(main, "Scrounge for Stones   ", "slate gray", gv.STONES_ICON,
                                       compound="right", cmd=None, activebackground="dim gray")
    stone_btn.configure(command=partial(
        create_thread, (partial(upd, stone_bar, 1, stone_btn, gather_stone, True))))
    stone_lbl = create_resource_label(main, stones, "slate gray")
    stone_btn.place(x=50, y=150)
    stone_lbl.place(x=310, y=150)
    opt_icon = tk.PhotoImage(file=gv.SETTINGS_GEAR)
    opt_btn = tk.Button(main, image=opt_icon,
                        command=partial(opt_menu, main), bg="springgreen4",
                        bd=0, fg="red", activebackground="springgreen4")
    stick_bar.place(x=50, y=120)
    stone_bar.place(x=50, y=220)
    stone_blades_str.set(f"Stone Blades: {stone_blades.get()}")
    stone_b_lbl = tk.Label(main, textvariable=stone_blades_str, font=(
        gv.def_font, 18, "bold"), padx=2)
    stone_b_lbl.place(x=500, y=50)
    opt_btn.image = opt_icon
    opt_btn.pack(side="top", anchor="ne", padx=10, pady=10)
    stone_knap_btn = tk.Button(
        main, text="Knap Stone (min 2 stones)", command=partial(stone_knapping, main))
    stone_knap_btn.pack(side="top", anchor="ne", padx=25, pady=10)
    # root.withdraw()
    main.deiconify()


def gather_stick():
    if gv.gather_tool == None:
        sticks.set(sticks.get() + 1)
    root.update_idletasks()


def gather_stone():
    if gv.gather_tool == None:
        stones.set(stones.get() + 1)
    root.update_idletasks()


def play_sound(file, wait=False):
    sound = sa.WaveObject.from_wave_file(file)
    player = sound.play()
    if wait == True:
        player.wait_done()


def cntr_wnd(wnd):
    x = ((gv.screen_width // 2) - (wnd.winfo_reqwidth() // 2))
    y = ((gv.screen_height // 2) - (wnd.winfo_reqheight() // 2))
    wnd.geometry(f"{wnd.winfo_reqwidth()}x{wnd.winfo_reqheight()}+{x}+{y}")


def dstr_wnd(wnd, p_wnd=None, pnoise=True):
    if pnoise == True:
        play_sound(gv.NEG_MENU)
    if p_wnd:
        p_wnd.focus_force()
    wnd.destroy()


def return_to_mm(wind, cscrn):
    root.deiconify()
    dstr_wnd(wind)
    dstr_wnd(cscrn, pnoise=False)
    gv.mm_vis = True


def reset_vars():
    gv.has_save = False
    for v in gv.resource_vars:
        v.set(0)


def res_menu(wnd, p_wnd, res):
    dstr_wnd(wnd, root, False)
    if p_wnd != root:
        dstr_wnd(p_wnd, root, False)
    else:
        if res:
            start_game()
        else:
            dstr_wnd(wnd)
    if res:
        reset_vars()


def confirm_menu(p_wnd):
    if p_wnd == root:
        if gv.has_save == False:
            start_game()
            return None
    confirmed = False
    if p_wnd != root:
        p_wnd.withdraw()
    cnf = tk.Toplevel(p_wnd, background="gray20", relief="ridge", bd=3)
    cnf.configure(width=gv.WND_SMALL[0], height=gv.WND_SMALL[1]+10)
    cnf.resizable(False, False)
    cnf.grab_set()
    cnf.overrideredirect(True)
    cntr_wnd(cnf)
    cnf.focus_force()
    cnf_lbl = tk.Label(cnf, text="Are you sure?",
                       bg="gray20", font=(gv.def_font, 32, "bold"), fg="red2")
    cnf_lbl.pack(side="top")
    disc_lbl = tk.Label(cnf, text="By pressing \"I'm sure\" you understand\nthat any progress you have will be reset", font=(
        gv.def_font, 18, "bold"), bg="gray20", fg="red3")
    disc_lbl.pack(side="top", pady=5)
    y_btn = tk.Button(cnf, text="I'm sure", bg="red",
                      activebackground="red3", width=20, height=3, command=partial(res_menu, cnf, p_wnd, True))
    n_btn = tk.Button(cnf, text="Cancel", bg="olive drab",
                      activebackground="forest green", width=20, height=3, command=partial(res_menu, cnf, p_wnd, False))
    y_btn.pack(side="right", anchor="se", padx=10, pady=10)
    n_btn.pack(side="left", anchor="sw", padx=10, pady=10)


def opt_menu(pw):
    prev_wnd = pw
    options = tk.Toplevel(root, bg="chartreuse4", bd=20.0, relief="raised")
    options.withdraw()
    play_sound(gv.POS_MENU)
    options.configure(width=gv.WND_TALL[0], height=gv.WND_TALL[1])
    options.grab_set()
    options.resizable(False, False)
    options.update_idletasks()
    options.overrideredirect(True)
    cntr_wnd(options)
    if gv.mm_vis == False:
        bk_btn = tk.Button(options, font=(gv.def_font, 24, "bold"), text="X", image=PXL_SIZER, compound='c', background="dark olive green", activebackground="dark green", foreground="firebrick4",
                           command=partial(dstr_wnd, options, prev_wnd), padx=10, height=20, relief="ridge", bd=1).pack(side="top", anchor="ne")
        opt_ttl = tk.Label(options, text="Options", font=(
            gv.def_font, 60, "bold"), background="chartreuse4").pack(side="top")
        mm_btn = tk.Button(options, font=(gv.def_font, 24, "bold"), text="Main Menu", image=PXL_SIZER, compound='c', height=35, background="red3", activebackground="red4", padx=15, command=partial(
            return_to_mm, options, prev_wnd)).pack(side="bottom", pady=15)
    elif gv.mm_vis == True:
        bk_btn = tk.Button(options, text="Back", background="firebrick3",
                           command=partial(dstr_wnd, options, prev_wnd),
                           padx=10, pady=10, relief="ridge", bd=1
                           ).pack(side="bottom", pady=40)
        rst_btn = tk.Button(options, text="Reset?", background="red",
                            command=partial(confirm_menu, options))
        opt_ttl = tk.Label(options, text="Options", font=(
            gv.def_font, 60, "bold"), background="chartreuse4").pack(side="top")
        rst_btn.pack(side="bottom", pady=30)
    options.deiconify()

# endregion Function Definitions


if __name__ == "__main__":
    root = tk.Tk()
    # region create resource vars
    sticks = tk.IntVar()
    sticks.set(0)
    gv.resource_vars.append(sticks)
    stones = tk.IntVar()
    stones.set(0)
    gv.resource_vars.append(stones)
    stone_blades = tk.IntVar()
    stone_blades.set(0)
    stone_blades_str = tk.StringVar()
    gv.resource_vars.append(stone_blades)
    # endregion
    # region create pg_bar styles
    stick_sty = ttk.Style()
    stick_sty.theme_use("default")
    stick_sty.configure(style="stick.Horizontal.TProgressbar",
                        background="saddlebrown", pbarrelief="ridge", thickness=1)
    stone_sty = ttk.Style()
    stone_sty.theme_use("default")
    stone_sty.configure(style="stone.Horizontal.TProgressbar",
                        background="slate gray", pbarrelief="ridge", thickness=1)
    # endregion
    PXL_SIZER = tk.PhotoImage(width=1, height=1)
    root.attributes("-fullscreen", True)
    root.configure(background=gv.bgc)

    # region Main Menu
    ttl = tk.Label(root, text="Vintage Incremental", font=(gv.def_font, 60, "bold"),
                   background=gv.bgc).pack(side="top", pady=80)
    exit_btn = tk.Button(root, text="Quit", font=(
        gv.def_font, 24), command=exit_game, padx=50, background="firebrick3", activebackground="firebrick4",
        relief="ridge", bd=5).pack(side="bottom", pady=15)
    strt_btn = tk.Button(root, text="New Game", font=(
        gv.def_font, 24), command=partial(confirm_menu, root), background="olive drab", activebackground="forestgreen",
        padx=80)
    strt_btn.pack(side="top", pady=40)
    ctn_btn = tk.Button(root, text="Continue", font=(
        gv.def_font, 24), command=start_game, background="snow4", activebackground="grey36",
        padx=80).pack(side="top")
    opt_btn = tk.Button(root, text="Options", font=(
        gv.def_font, 24), command=partial(opt_menu, root), background="mediumorchid3", activebackground="mediumorchid4",
        padx=80).pack(side="top", pady=120)

    # endregion Main Menu

    root.mainloop()
