import numpy as np
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W
from PIL import Image, ImageTk
import logic


class ManualGUI(tk.Frame):
    def __init__(self, window, nextScreen):
        tk.Frame.__init__(self, window)
        self.config(bg="#464646")
        # Tile Mod Dropdown
        # Vars
        self.nextScreen = nextScreen
        self.north_tile = tk.StringVar(value="void")
        self.east_tile = tk.StringVar(value="void")
        self.south_tile = tk.StringVar(value="void")
        self.west_tile = tk.StringVar(value="void")
        # Init
        north_tile_dropdown = ttk.Combobox(self, textvariable=self.north_tile, width=7)
        east_tile_dropdown = ttk.Combobox(self, textvariable=self.east_tile, width=7)
        south_tile_dropdown = ttk.Combobox(self, textvariable=self.south_tile, width=7)
        west_tile_dropdown = ttk.Combobox(self, textvariable=self.west_tile, width=7)
        # Options
        self.dropdowns = (north_tile_dropdown, east_tile_dropdown, south_tile_dropdown, west_tile_dropdown)
        for dropdown in self.dropdowns:
            dropdown['values'] = tile_methods
            dropdown.current(0)
            dropdown.bind("<<ComboboxSelected>>", self.on_arguments_change)
        # Location
        north_tile_dropdown.grid(column=1, row=0, sticky=S, padx=70, pady=(10, 0))
        east_tile_dropdown.grid(column=2, row=1, sticky=W, padx=(0, 70), pady=10)
        south_tile_dropdown.grid(column=1, row=2, sticky=N, padx=70, pady=(0, 10))
        west_tile_dropdown.grid(column=0, row=1, sticky=E, padx=(50, 0), pady=10)

        # Algorithm Dropdown
        self.algorithm = tk.StringVar()  # Var
        ttk.Label(self, text="Algorithm:").grid(column=0, row=5, sticky=W + E, padx=30, pady=(10, 0))  # Label
        algorithm_dropdown = ttk.Combobox(self, textvariable=self.algorithm, width=5)  # Init
        algorithm_dropdown['values'] = ("xBR", "xBRZ")  # Options
        algorithm_dropdown.current(1)
        algorithm_dropdown.bind("<<ComboboxSelected>>", self.on_arguments_change)
        algorithm_dropdown.grid(column=0, row=6, padx=30, pady=(0, 10))  # Location

        # Preset Dropdown
        self.preset = tk.StringVar()  # Var
        self.preset_dropdown = ttk.Combobox(self, textvariable=self.preset, width=10)  # Init
        self.preset_dropdown['values'] = list(preset_dict)  # Options
        self.preset_dropdown.current(1)
        self.preset_dropdown.bind("<<ComboboxSelected>>", self.on_set_preset)
        self.preset_dropdown.grid(column=0, row=0, padx=30, pady=(10, 0))  # Location

        # Unscaled Image
        raw_image = ImageTk.PhotoImage(
            image=Image.new(size=(1, 1), mode="RGBA", color="#000000"))  # temp image, never shown
        self.raw_image_label = tk.Label(self, image=raw_image)
        self.raw_image_label.image = raw_image
        self.raw_image_label.config(bg="#333333")
        self.raw_image_label.grid(column=1, row=1)
        # Tile Preview Image
        tile_preview_image = ImageTk.PhotoImage(
            image=Image.new(size=(1, 1), mode="RGBA", color="#000000"))  # temp image, never shown
        self.tile_preview_label = tk.Label(self, image=tile_preview_image)
        self.tile_preview_label.image = tile_preview_image
        self.tile_preview_label.config(bg="#262626")
        self.tile_preview_label.grid(column=2, row=0, padx=30, pady=10)
        # Upscaled Image
        scaled_image = ImageTk.PhotoImage(
            image=Image.new(size=(1, 1), mode="RGBA", color="#000000"))  # temp image, never shown
        self.scaled_image_label = tk.Label(self, image=scaled_image)
        self.scaled_image_label.image = scaled_image
        self.scaled_image_label.config(bg="#333333")
        self.scaled_image_label.grid(column=3, row=1, padx=(0, 30))

        # Path to image
        self.image_path_label = ttk.Label(self, text="you shouldn't see this", justify="center", wraplength=256)
        self.image_path_label.grid(column=3, row=2, sticky=W + E, padx=(0, 30), pady=(0, 10))

        # Skip image button (leaves it not upscaled)
        nextButton = ttk.Button(self, text='skip', command=self.skip_image)
        nextButton.grid(column=1, row=6, sticky=W + E, padx=30, pady=10)
        # Next image button
        nextButton = ttk.Button(self, text='next', command=self.next_image)
        nextButton.grid(column=2, row=6, columnspan=2, sticky=W + E, padx=30, pady=10)

        # Back button
        self.backButton = ttk.Button(self, text='back', command=self.previous_image)
        self.backButton.grid(column=3, row=0, columnspan=2, sticky=W + E, padx=30, pady=10)
        self.backButton["state"] = "disabled"


    def get_args(self):
        return {
            "nTile": self.north_tile.get(),
            "eTile": self.east_tile.get(),
            "sTile": self.south_tile.get(),
            "wTile": self.west_tile.get(),
            "algorithm": self.algorithm.get()
        }

    # called on setting preset
    def on_set_preset(self, event):
        for i in range(len(preset_dict[self.preset.get()])):
            # the only reason this is so ugly is that you can't set a Combobox using the desired value, you have to set it using the index of the desired value
            # basically, given our current preset, get the relevant tile setting
            # given that relevant tile setting get its index for the combobox
            self.dropdowns[i].current(tile_methods.index(preset_dict[self.preset.get()][i]))
        logic.update_preview()

    # called whenever any variable is changed
    def on_arguments_change(self, event):
        self.preset_dropdown.current(list(preset_dict).index("custom"))
        logic.update_preview()

    # called by logic.updatePreview()
    def update_preview(self, raw_image_path, scaled_image_path):
        if logic.imageIndex > 0:
            self.backButton["state"] = "normal"
        else:
            self.backButton["state"] = "disabled"

        img_dimensions = Image.open(raw_image_path).size
        new_width = int((256 * img_dimensions[0] / img_dimensions[1]))

        raw_image = ImageTk.PhotoImage(image=Image.open(raw_image_path).resize((new_width, 256), Image.NEAREST))
        self.raw_image_label.config(image=raw_image, width=256, height=256)
        self.raw_image_label.image = raw_image

        scaled_image = ImageTk.PhotoImage(image=Image.open(scaled_image_path).resize((new_width, 256), Image.NEAREST))
        self.scaled_image_label.config(image=scaled_image, width=256, height=256)
        self.scaled_image_label.image = scaled_image

        self.image_path_label.config(text=raw_image_path.replace(logic.pack_location + "\\", ""))

    def update_tile_preview(self, scaled_image_path):
        img_dimensions = Image.open(scaled_image_path).size
        new_width = int((96 * img_dimensions[0] / img_dimensions[1]))

        tile_preview_image = ImageTk.PhotoImage(image=Image.open(scaled_image_path).resize((new_width, 96), Image.NEAREST))
        self.tile_preview_label.config(image=tile_preview_image, width=96, height=96)
        self.tile_preview_label.image = tile_preview_image

    # called on pressing the "next" button
    @staticmethod
    def next_image():
        logic.next_image()

    # called on pressing the "skip" button
    @staticmethod
    def skip_image():
        logic.skip_image()

    @staticmethod
    def previous_image():
        logic.previous_image()


# the keys of image_processing.tile_dict in order
tile_methods = ["void", "wrap", "extend", "mirror"]

# the tiling for each direction in North East South West order
preset_dict = {
    "block": ["wrap", "wrap", "wrap", "wrap"],

    "item": ["void", "void", "void", "void"],

    "fauna": ["void", "void", "extend", "void"],

    "custom": []
}
