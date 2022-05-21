from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W
from PIL import Image, ImageTk

# TODO shgdtfuoinpjgsredjuhiodgsruodhpijhgsrtdeuiop
scaleFactor = 4

def manualPage(window, nextScreen):
    # Called when we run out of images to upscale
    # - Gathers important variables
    # - Moves to next screen
    def nextScreen():
        args = {
        }
        print(args)
        nextScreen(args, "manual")

    northTile = tk.StringVar(value="void")
    eastTile = tk.StringVar(value="void")
    southTile = tk.StringVar(value="void")
    westTile = tk.StringVar(value="void")

    northTile_dropdown = ttk.Combobox(window, textvariable=northTile, width=7)
    eastTile_dropdown = ttk.Combobox(window, textvariable=eastTile, width=7)
    southTile_dropdown = ttk.Combobox(window, textvariable=southTile, width=7)
    westTile_dropdown = ttk.Combobox(window, textvariable=westTile, width=7)

    dropdowns = (northTile_dropdown, eastTile_dropdown, southTile_dropdown, westTile_dropdown)
    for dropdown in dropdowns:
        dropdown['values'] = ("void",
                              "wrap",
                              "extend",
                              "mirror")

    northTile_dropdown.grid(column=1, row=0, sticky=W + E, padx=70, pady=(10, 0))
    eastTile_dropdown.grid(column=2, row=1, sticky=W + E, padx=(0, 30), pady=10)
    southTile_dropdown.grid(column=1, row=2, sticky=W + E, padx=70, pady=(0, 10))
    westTile_dropdown.grid(column=0, row=1, sticky=W + E, padx=(50, 0), pady=10)

    # Algorithm Dropdown
    # Label
    ttk.Label(window, text="Algorithm:").grid(column=0, row=5, sticky=W + E, padx=30, pady=(10, 0))
    # Dropdown
    algorithm = tk.StringVar(value="xbr")
    algorithm_dropdown = ttk.Combobox(window, textvariable=algorithm, width=5)
    algorithm_dropdown['values'] = ("xbr", "xbrz")
    algorithm_dropdown.grid(column=0, row=6, sticky=W + E, padx=30, pady=(0, 10))

    # Path to image
    ttk.Label(window, text="minecraft/textures/block/sculk_catalyst_top.png", justify="center").grid(column=3, row=2, sticky=W + E, padx=30, pady=(0, 10))

    # Unscaled Image
    unscaled = Image.open("sculk_catalyst_top.png")
    unscaled = ImageTk.PhotoImage(image=unscaled.resize((unscaled.width * scaleFactor * 3, unscaled.height * scaleFactor * 3), Image.NEAREST))
    unscaledLabel = tk.Label(window, image=unscaled)
    unscaledLabel.image = unscaled
    unscaledLabel.config(bg="#464646")
    unscaledLabel.grid(column=1, row=1)

    # Upscaled Image
    upscaled = Image.open("sculk_catalyst_top_xbr.png")
    upscaled = ImageTk.PhotoImage(image=upscaled.resize((upscaled.width * 3, upscaled.height * 3), Image.NEAREST))
    upscaledLabel = tk.Label(window, image=upscaled)
    upscaledLabel.image = upscaled
    upscaledLabel.config(bg="#464646")
    upscaledLabel.grid(column=3, row=1, padx=(0, 30))

    # Skip image button (leaves it not upscaled)
    nextButton = ttk.Button(window, text='skip')
    nextButton.grid(column=1, row=6, sticky=W + E, padx=30, pady=10)
    nextButton["state"] = "disabled"

    # Next image button
    nextButton = ttk.Button(window, text='next')
    nextButton.grid(column=2, row=6, columnspan=2, sticky=W + E, padx=30, pady=10)
    nextButton["state"] = "disabled"

    return window
