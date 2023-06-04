import time
import ctypes.wintypes as wintypes
import keyboard
import pyautogui
import win32gui
import win32gui as gui
import sys
import logging
import win32com.client
from pywinauto import Desktop
from win32api import GetSystemMetrics

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

currentWindowIndex = 0


def move_window(pos_x=0, pos_y=0, move=50):
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        # time.sleep(0.01)w
        window = gui.GetForegroundWindow()
        active_window_name = gui.GetWindowText(window)
        tup = win32gui.GetWindowPlacement(window)
        print(active_window_name)
        # print(active_window_name)
        x, y, w, h = get_window_pos(window)
        dis_w, dis_h = get_monitor_resolution()
        if tup[1] == 3:
            win_place_list = list(tup)
            win_place_list[1] = 1
            tup = tuple(win_place_list)
            win32gui.SetWindowPlacement(window, win_place_list)
            print(f"window is = {tup[1]}")

        if pos_y > 50 and y > -8:
            gui.MoveWindow(window, x, y - move, w, h, True)
            # print(f"{x}, {y}, {w}, {h}")
            # print("up")
        if pos_y < -10 and y < (dis_h - 50):
            gui.MoveWindow(window, x, y + move, w, h, True)
            # print(f"{x}, {y}, {w}, {h}")
            # print("down")
        if pos_x > 50 and x < (dis_w - 50):
            gui.MoveWindow(window, x + move, y, w, h, True)
            # print(f"{x}, {y}, {w}, {h}")
            # print("right")
        if pos_x < -20 and x > -8:
            gui.MoveWindow(window, x - move, y, w, h, True)
            # print(f"{x}, {y}, {w}, {h}")
            # print("left")
        # print(f"h = {dis_h}, w = {dis_w}")
        if keyboard.is_pressed('alt+w') and y > -8:
            gui.MoveWindow(window, x, y - move, w, h, True)
            print(f"{x}, {y}, {w}, {h}")
        if keyboard.is_pressed('alt+s') and y < dis_h - 10:
            gui.MoveWindow(window, x, y + move, w, h, True)
            print(f"{x}, {y}, {w}, {h}")
        if keyboard.is_pressed('alt+a') and x > -8:
            gui.MoveWindow(window, x - move, y, w, h, True)
            print(f"{x}, {y}, {w}, {h}")
        if keyboard.is_pressed('alt+d') and x < dis_w - 10:
            gui.MoveWindow(window, x + move, y, w, h, True)
            print(f"{x}, {y}, {w}, {h}")


def get_window_pos(window):
    time.sleep(0.01)
    rect = gui.GetWindowRect(window)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    return x, y, w, h


def move_window_back():
    window = gui.GetForegroundWindow()
    x, y, w, h = get_window_pos(window)
    gui.MoveWindow(window, 250, 250, w, h, True)


def getAllWindows():
    hwndList = list()

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            hwndList.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)

    for i, window in enumerate(hwndList):
        windowText = str(win32gui.GetWindowText(window))
        # print(len(windowText) > 0)
        # if len(windowText) > 0:
        #     print(win32gui.GetWindowText(window))

        if gui.GetWindowTextLength(window) == 0:
            hwndList.pop(i)
            # print("pop")
        elif (windowText == 'C:\\Users\\bhuva\\Documents\\Rainmeter\\Skins\\Ultralight\\Ultralight Clock\\Ultralight '
                            'clock.ini' or windowText == 'Taskbar' or windowText == 'Program Manager'):
            # print(windowText)
            # print("pop1")
            hwndList.pop(i)

    return hwndList

    # for w in hwndList:
    #     print(gui.GetWindowText(w))


def getWindows():
    winList = getAllWindows()
    # print(winList)
    i = 0
    for win in winList:
        windowText = gui.GetWindowText(win)
        if gui.GetWindowTextLength(win) == 0:
            winList.pop(i)
            # print("pop")
        elif (windowText == 'C:\\Users\\bhuva\\Documents\\Rainmeter\\Skins\\Ultralight\\Ultralight Clock\\Ultralight '
                            'clock.ini' or windowText == 'Taskbar' or windowText == 'Program Manager'):
            # print(windowText)
            # print("pop1")
            winList.pop(i)
        i += 1
    i = 0
    for win in winList:
        windowText = gui.GetWindowText(win)
        if gui.GetWindowTextLength(win) == 0:
            winList.pop(i)
            # print("pop")
        elif (windowText == 'C:\\Users\\bhuva\\Documents\\Rainmeter\\Skins\\Ultralight\\Ultralight Clock\\Ultralight '
                            'clock.ini' or windowText == 'Taskbar' or windowText == 'Program Manager'):
            # print(windowText)
            # print("pop1")
            winList.pop(i)
        i += 1
    i = 0
    for win in winList:
        windowText = gui.GetWindowText(win)
        if gui.GetWindowTextLength(win) == 0:
            winList.pop(i)
            # print("pop")
        elif (windowText == 'C:\\Users\\bhuva\\Documents\\Rainmeter\\Skins\\Ultralight\\Ultralight Clock\\Ultralight '
                            'clock.ini' or windowText == 'Taskbar' or windowText == 'Program Manager'):
            # print(windowText)
            # print("pop1")
            winList.pop(i)
        i += 1

    return winList


def switchWindow(window):
    w = WindowMgr()
    w.find_window_wildcard(gui.GetWindowText(window))


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if wildcard == gui.GetWindowText(hwnd):
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        self.set_foreground()

    def set_foreground(self):
        """put the window in the foreground"""
        try:
            print(gui.GetWindowText(self._handle) + "s")
            self.shell.SendKeys('%')
            win32gui.SetForegroundWindow(self._handle)
        except:
            print("error")


def get_monitor_resolution():
    from screeninfo import get_monitors
    displayHeight = 0
    displayWidth = 0
    for m in get_monitors():
        displayHeight = m.height
        displayWidth += m.width

    return displayWidth, displayHeight


if __name__ == "__main__":
    # windows = getWindows()
    # for win in windows:
    #     print(gui.GetWindowTextLength(win))
    # windowCount = 0

    while True:
        if keyboard.is_pressed('alt+r'):
            move_window()
        time.sleep(0.01)
    #     if keyboard.is_pressed('alt+p'):
    #         switchWindow(windows[windowCount])
    #         windowCount += 1
    #         if windowCount > (len(windows) - 1):
    #             windowCount = 0
