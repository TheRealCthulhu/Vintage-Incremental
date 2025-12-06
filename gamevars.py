import pyautogui as pg
def_font = 'Gabriola'
bgc = "dark olive green"
screen_width = pg.size()[0]
screen_height = pg.size()[1]
prev_wnd = None
gather_tool = None
mm_vis = True
has_save = False
resource_vars = []


# region Constants
WND_SMALL = (screen_width // 4, screen_height // 4)
WND_TALL = (screen_width // 4, screen_height // 1.5)
WND_SQUARE = (screen_width // 4)
POS_MENU = "_internal/Sounds/UI/Modern2.wav"
NEG_MENU = "_internal/Sounds/UI/Modern3.wav"
START_SOUND = "_internal/Sounds/UI/Wood_Block1.wav"
SETTINGS_GEAR = "_internal/assets/settings_gear.gif"
STICK_ICON = "_internal/assets/stick.png"
STONES_ICON = "_internal/assets/stones.png"
RECIPES = {"TWO_STONE_BLADE_RECIPE": ([[True, False, False, False, True], [True, True, False, True, True], [
    True, True, False, True, True], [True, True, False, True, True], [True, True, False, True, True]], "2x Stone Blade"), "ONE_STONE_BLADE_RECIPE": ([[True, False, False, False, False], [True, True, False, False, False], [
        True, True, False, False, False], [True, True, False, False, False], [True, True, False, False, False]], "1x Stone Blade"), "ALT_ONE_STONE_BLADE_RECIPE": ([[False, False, False, False, True], [False, False, False, True, True], [
            False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True]], "1x Stone Blade")}
# endregion
