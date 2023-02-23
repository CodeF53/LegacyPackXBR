from tkinterdnd2 import TkinterDnD
import tkinter as tk
from ttkthemes import ThemedStyle

# internal methods
import logic
from exit import exit_screen
from ttkShit import dark_title
from config import configPage
from manual import ManualGUI
from auto import AutoGUI
from logic import init_logic


def nextScreen(args, screen):
  if screen == "config":
    # Stop rendering
    configScreen.destroy()

    global autoScreen, manualScreen

    if args.get("auto"):
      raise Exception("auto is not yet implemented for PackXBR GUI")
      # autoScreen = AutoGUI(window, nextScreen)
      # init_logic(args, autoScreen)
      # autoScreen.pack(expand=1, fill=tk.BOTH)
    else:
      manualScreen = ManualGUI(window, nextScreen)
      init_logic(args, manualScreen)
      manualScreen.pack(expand=1, fill=tk.BOTH)
  if screen == "manual":
    # Stop rendering
    manualScreen.destroy()

    # Show exit screen
    exit_screen(tk.Canvas(window, bg="#464646", borderwidth=0, highlightthickness=0), args).pack(expand=1, fill=tk.BOTH)


# Establish window parameters
root = TkinterDnD.Tk()
root.title("PackXBR")
root.resizable(False, False)
# set it in the center of the screen
root.geometry(f"+{int(root.winfo_screenwidth()/2) - 131}+{int(root.winfo_screenheight()/2) - 132}")
# Set theme
root.config(bg="#464646")
ThemedStyle(root).set_theme("equilux")
root.iconbitmap(logic.resource_path("packXBR.ico"))
# Dark title bar
window = dark_title(root)

configScreen = configPage(tk.Canvas(window, bg="#464646", borderwidth=0, highlightthickness=0), nextScreen)
configScreen.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
  root.mainloop()
