import tkinter.ttk as ttk


def exit_screen(window, args):
    pack_location = args["pack_location"]

    ttk.Label(window, text="DONE!", font=("Default", 30)).grid(column=0, row=0, padx=30, pady=10)
    ttk.Label(window, text=f"you can find your finished pack at {pack_location}").grid(column=0, row=1, padx=30,
                                                                                       pady=10)

    return window
