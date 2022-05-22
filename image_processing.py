# Libraries:
import os
import sys
import subprocess
import traceback

import numpy as np
from PIL import Image


def process_image(args, img_raw_path, img_scaled_path, scale_factor):
    # get image in array
    img = np.asarray(Image.open(img_raw_path).convert('RGBA'))
    img_height, img_width = img.shape[0:2]

    # tile
    img = tileDict[args["nTile"]](img, [1, 0, 0, 0], img_height, img_width)
    img = tileDict[args["sTile"]](img, [0, 1, 0, 0], img_height, img_width)
    img = tileDict[args["eTile"]](img, [0, 0, 0, 1], img_height, img_width)
    img = tileDict[args["wTile"]](img, [0, 0, 1, 0], img_height, img_width)

    # save
    Image.fromarray(img).save(img_scaled_path)

    # xbr
    xbr(input_path = img_scaled_path, output_path = img_scaled_path, algorithm=args["algorithm"], scale_factor = scale_factor)
    # crop in

    # save

def tile_GENERIC(img, direction, width, height, method):
    return np.pad(img, ((direction[0] * height, direction[1] * height), (direction[2] * width, direction[3] * width), (0, 0)), method)

tileDict = {
    "void": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "constant"),
    "wrap": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "wrap"),
    "extend": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "edge"),
    "mirror": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "symmetric")
}


# Fixes directories of local files when compiled into auto-py-to-exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyUnresolvedReferences
        base_path = sys._MEIPASS
    except Exception:
        # If the above fails, it means we aren't compiled, so paths work normally
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Calls ScalerTest_Windows.exe with the proper args
def xbr(input_path, output_path, algorithm, scale_factor):
    try:
        arguments = f"-{scale_factor}{algorithm} \"{input_path}\" \"{output_path}\""
        print(arguments)
        subprocess.check_output(  # launch a process with args, pausing main thread until process is finished
            "ScalerTest_Windows.exe " +  # resource_path("ScalerTest_Windows.exe") +  # call in a way that works with files packed into an exe
            arguments,  # args for xBRz on our image
            creationflags=0x08000000)  # don't show the console window doing this.
    except Exception:
        traceback.print_exc()
        exit()


if __name__ == '__main__':
    args = {
        "nTile": "void",
        "eTile": "void",
        "sTile": "void",
        "wTile": "void",
        "algorithm": "xbr"
    }
    process_image(args, "test/raw_iron.png", "test/raw_iron_out.png")
