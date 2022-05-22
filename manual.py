from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W
from PIL import Image, ImageTk

import logic


class ManualGUI(tk.Frame):
    def __init__(self, window, externalNextScreen):
        tk.Frame.__init__(self, window)
        self.config(bg="#464646")
        # Tile Mod Dropdown
        # Vars
        self.externalNextScreen = externalNextScreen
        self.northTile = tk.StringVar(value="void")
        self.eastTile = tk.StringVar(value="void")
        self.southTile = tk.StringVar(value="void")
        self.westTile = tk.StringVar(value="void")
        # Init
        northTile_dropdown = ttk.Combobox(self, textvariable=self.northTile, width=7)
        eastTile_dropdown = ttk.Combobox(self, textvariable=self.eastTile, width=7)
        southTile_dropdown = ttk.Combobox(self, textvariable=self.southTile, width=7)
        westTile_dropdown = ttk.Combobox(self, textvariable=self.westTile, width=7)
        # Options
        dropdowns = (northTile_dropdown, eastTile_dropdown, southTile_dropdown, westTile_dropdown)
        for dropdown in dropdowns:
            dropdown['values'] = ("void", "wrap", "extend", "mirror")
            dropdown.current(0)
            dropdown.bind("<<ComboboxSelected>>", self.fhjdtgy)
        # Location
        northTile_dropdown.grid(column=1, row=0, sticky=W + E, padx=70, pady=(10, 0))
        eastTile_dropdown.grid(column=2, row=1, sticky=W + E, padx=(0, 30), pady=10)
        southTile_dropdown.grid(column=1, row=2, sticky=W + E, padx=70, pady=(0, 10))
        westTile_dropdown.grid(column=0, row=1, sticky=W + E, padx=(50, 0), pady=10)

        # Algorithm Dropdown
        self.algorithm = tk.StringVar()  # Var
        ttk.Label(self, text="Algorithm:").grid(column=0, row=5, sticky=W + E, padx=30, pady=(10, 0))  # Label
        algorithm_dropdown = ttk.Combobox(self, textvariable=self.algorithm, width=5)  # Init
        algorithm_dropdown['values'] = ("xBR", "xBRZ")  # Options
        algorithm_dropdown.current(0)
        algorithm_dropdown.bind("<<ComboboxSelected>>", self.fhjdtgy)
        algorithm_dropdown.grid(column=0, row=6, sticky=W + E, padx=30, pady=(0, 10))  # Location

        # Path to image
        ttk.Label(self, text="i/need/to/change/shit/to/get/this/to/work.png", justify="center").\
            grid(column=3, row=2, sticky=W + E, padx=30, pady=(0, 10))

        # Unscaled Image
        rawImage = Image.open("sculk_catalyst_top.png")
        rawImage = ImageTk.PhotoImage(image=rawImage.resize((256, 256), Image.NEAREST))
        self.rawLabel = tk.Label(self, image=rawImage)
        self.rawLabel.image = rawImage
        self.rawLabel.config(bg="#464646")
        self.rawLabel.grid(column=1, row=1)

        # Upscaled Image
        upscaled = Image.open("sculk_catalyst_top_xbr.png")
        upscaled = ImageTk.PhotoImage(image=upscaled.resize((256, 256), Image.NEAREST))
        self.scaledLabel = tk.Label(self, image=upscaled)
        self.scaledLabel.image = upscaled
        self.scaledLabel.config(bg="#464646")
        self.scaledLabel.grid(column=3, row=1, padx=(0, 30))

        # Skip image button (leaves it not upscaled)
        nextButton = ttk.Button(self, text='skip')
        nextButton.grid(column=1, row=6, sticky=W + E, padx=30, pady=10)
        nextButton["state"] = "disabled"

        # Next image button
        nextButton = ttk.Button(self, text='next')
        nextButton.grid(column=2, row=6, columnspan=2, sticky=W + E, padx=30, pady=10)
        nextButton["state"] = "disabled"

    def getArgs(self):
        return {
            "nTile": self.northTile.get(),
            "eTile": self.eastTile.get(),
            "sTile": self.southTile.get(),
            "wTile": self.westTile.get(),
            "algorithm": self.algorithm.get()
        }

    # called whenever any variable is changed
    @staticmethod
    def fhjdtgy(event):
        logic.update_preview()

    # called by logic.updatePreview()
    def update_preview(self, rawImagePath, scaledImagePath):
        rawImage = ImageTk.PhotoImage(image=Image.open(rawImagePath).resize((256, 256), Image.NEAREST))
        self.rawLabel.config(image=rawImage)
        self.rawLabel.image = rawImage

        scaledImage = ImageTk.PhotoImage(image=Image.open(scaledImagePath).resize((256, 256), Image.NEAREST))
        self.scaledLabel.config(image=scaledImage)
        self.scaledLabel.image = scaledImage




def manualPage(window, externalNextScreen):
    # Called when we run out of images to upscale
    # - Gathers important variables
    # - Moves to next screen
    def nextScreen():
        args = {
        }
        print(args)
        externalNextScreen(args, "manual")

    return window
