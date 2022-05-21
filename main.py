from tkinterdnd2 import TkinterDnD
import tkinter as tk
from ttkthemes import ThemedStyle

# internal methods
from ttkShit import darkTitle
from config import configPage
from manual import manualPage


def nextScreen(args, screen):
    if screen == "config":
        configPage.destroy()
        if args.get("auto"):
            raise Exception("auto is not yet implemented for PackXBR GUI")
        else:
            manualPage.pack(expand=1, fill=tk.BOTH)


# Establish window parameters
root = TkinterDnD.Tk()
root.title("PackXBR")
root.resizable(False, False)
# Set theme
root.config(bg="#464646")
ThemedStyle(root).set_theme("equilux")
# Dark title bar
window = darkTitle(root)

configPage = configPage(tk.Canvas(window, bg="#464646", borderwidth=0, highlightthickness=0), nextScreen)
configPage.pack(expand=1, fill=tk.BOTH)
manualPage = manualPage(tk.Canvas(window, bg="#464646", borderwidth=0, highlightthickness=0), nextScreen)
#manualPage.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
    root.mainloop()
