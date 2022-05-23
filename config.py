from tkinterdnd2 import DND_FILES
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W
from os.path import exists, isdir
# internal methods
from ttkShit import multiple_choice


def configPage(window, externalNextScreen):
    # Called when "next" button is pressed
    # - Gathers important variables
    # - Moves to next screen
    def nextScreen():
        args = {
            "packLocation": packLocation.get(),
            "scaleFactor": scaleFactor.get(),
            "auto": auto.get()
        }
        print(args)
        externalNextScreen(args, "config")

    # \\\\\\\\\\\\\\\\ DRAG AND DROP STUFF /////////////////
    # Thank you, Ramon Williams for the excellent tutorial!
    # https://youtu.be/JIy0QjwQBl0
    # Called when new file is dragged and dropped into hole
    # - Sets hole to display dropped item
    # - Verifies Pack Location
    def dropPackLocation(dropped):
        # process out stupid stuff
        newData = dropped.data
        newData = newData.replace("{", "").replace("}", "")

        # update with processed data
        packLocation.set(newData)

        # verify location
        verifyPackLocation()

    # Checks if current PackLocation is a folder or string
    # - disables/enables the next button
    # - sets packLocation_valid
    # - sets packLocation_warning's text
    #   - if its invalid, display warning, if its valid be empty
    def verifyPackLocation(event=None):
        packPath = packLocation.get()

        if exists(packPath):
            if isdir(packPath) or packPath[-4:] == ".zip":
                nextButton["state"] = "normal"
                packLocation_warning.config(text="")
                return
        nextButton["state"] = "disabled"
        packLocation_warning.config(text=packLocation_warning_text_active)

    # Drag and drop pack input
    # Var and default value
    packLocation = tk.StringVar(value="Drag and Drop a Resource Pack Here")
    # Create
    packLocationBox = tk.Entry(window, textvariable=packLocation, width=34)
    packLocationBox.grid(column=0, row=0, columnspan=2, padx=10, pady=(10, 0), ipady=10)
    # Assign drag and drop register and method
    packLocationBox.drop_target_register(DND_FILES)
    packLocationBox.dnd_bind("<<Drop>>", dropPackLocation)
    # Set theme
    packLocationBox.configure(background="#535353", foreground="#BEBEBE", exportselection=False,
                              font=("Default", 10), relief="flat", justify="center")

    # Drag and drop pack input verification
    # Check if location valid after each keyrelease
    packLocationBox.bind('<KeyRelease>', verifyPackLocation)
    # Label
    packLocation_warning_text_active = "Resource Pack be a zip or folder"
    packLocation_warning = ttk.Label(window, text="")
    packLocation_warning.config(font=("Default", 8), foreground="red")
    packLocation_warning.grid(column=0, row=1, columnspan=2, padx=30, pady=(0, 10), sticky=W + E)

    # Multiple choice for scale factor
    # Label
    ttk.Label(window, text="Scale Factor:").grid(column=0, row=3, padx=30, pady=5, sticky=W + E)
    # Var and default value
    scaleFactor = tk.IntVar(value=4)
    # Create
    multiple_choice(root=window, variable=scaleFactor, options=("2x", "4x", "6x"), values=(2, 4, 6),
                    grid=((0, 4), (0, 5), (0, 6))
                    )

    # Multiple choice for mode
    # Label
    ttk.Label(window, text="Mode:").grid(column=1, row=3, padx=30, pady=5, sticky=W + E)
    # Var and default value
    auto = tk.BooleanVar(value=False)
    # Create
    multiple_choice(root=window, variable=auto, options=("Manual", "Auto"), values=(False, True),
                    grid=((1, 4), (1, 5))
                    )

    # Next screen button
    nextButton = ttk.Button(window, text='next', command=nextScreen)
    nextButton.grid(column=0, row=7, columnspan=2, sticky=W + E, padx=30, pady=10)
    nextButton["state"] = "disabled"

    return window
