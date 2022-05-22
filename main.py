from tkinterdnd2 import TkinterDnD
import tkinter as tk
from ttkthemes import ThemedStyle

# internal methods
from ttkShit import darkTitle
from config import configPage
from manual import ManualGUI
from logic import initLogic

def nextScreen(args, screen):
    if screen == "config":
        # Stop rendering
        configScreen.destroy()

        # Initialize internal upscaler
        initLogic(args, manualScreen)

        if args.get("auto"):
            raise Exception("auto is not yet implemented for PackXBR GUI")
        else:
            manualScreen.pack(expand=1, fill=tk.BOTH)


# Establish window parameters
root = TkinterDnD.Tk()
root.title("PackXBR")
root.resizable(False, False)
# Set theme
root.config(bg="#464646")
ThemedStyle(root).set_theme("equilux")
# Dark title bar
window = darkTitle(root)

configScreen = configPage(tk.Canvas(window, bg="#464646", borderwidth=0, highlightthickness=0), nextScreen)
configScreen.pack(expand=1, fill=tk.BOTH)
manualScreen = ManualGUI(window, nextScreen)
#manualScreen.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
    root.mainloop()
