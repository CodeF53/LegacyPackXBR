import numpy as np
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W
from PIL import Image, ImageTk
import logic

class AutoGUI(tk.Frame):
  def __init__(self, window, nextScreen):
    tk.Frame.__init__(self, window)
    self.config(bg="#464646")
    self.nextScreen = nextScreen

    while(True):
      logic.next_image()

  def get_args(self):
    return {
      "nTile": "wrap",
      "eTile": "wrap",
      "sTile": "wrap",
      "wTile": "wrap"
    }

if __name__ == '__main__':
  print("don't run this file on it's own, run main.py")
