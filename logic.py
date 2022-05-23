import sys
from os import startfile, path
from shutil import copytree, copy
from zipfile import ZipFile
from os.path import isfile, join
from os import walk, rename, remove
from glob import glob

# local imports
from image_processing import process_image

pack_location = ""
scale_factor = 4
imageLocations = []
imageIndex = -1

img_raw = ""
img_scaled = ""

screen = None


# Preps for upscaling
# - caches scale factor, pack location from args
# - unzips/clones to output directory -> "{packLocation}_xbr"
# - generates imageLocations
def init_logic(args, ManualGUI):
    global screen
    screen = ManualGUI
    # cache scale factor, pack location
    global pack_location, scale_factor, imageLocations
    pack_location = args.get("packLocation")
    scale_factor = args.get("scaleFactor")

    # unzip/clone to output directory -> "{packLocation}_xbr"
    if isfile(pack_location):
        # unzip to output directory
        ZipFile(pack_location, 'r').extractall(args.get("packLocation")[0:-4] + "_xbr")
        pack_location = pack_location[0:-4] + "_xbr"
    else:
        # clone to output directory
        copytree(src=pack_location, dst=pack_location + "_xbr")
        pack_location = pack_location + "_xbr"

    # generate list of locations to images
    # todo: ignore files with _xbr.png
    imageLocations = [y for x in walk(pack_location) for y in glob(join(x[0], '*.png'))]

    # prepare manual render previews
    initialize_next_image()

# deletes raw image and uses scaled image
# iterates imageIndex
def next_image():
    global img_raw, img_scaled
    #  -- This is now done when the pack is done --
    # put scaled image into place of raw image
    # remove(img_raw)
    # rename(img_scaled, img_raw)
    initialize_next_image()

# deletes scaled image and uses raw image
# iterates imageIndex
def skip_image():
    global img_scaled
    # delete scaled image
    remove(img_scaled)

    initialize_next_image()

# updates internal image variables
# ran by nextImage() and skipImage()
def initialize_next_image():
    global imageLocations, imageIndex
    global img_raw, img_scaled
    imageIndex = imageIndex + 1

    try:
        img_raw = imageLocations[imageIndex]
        img_scaled = img_raw.replace(".png", "_scaled.png")
        copy(img_raw, img_scaled)

        update_preview()
    except IndexError:
        # done upscaling!
        for img_raw_local in imageLocations:
            img_scaled_local = img_raw_local.replace(".png", "_scaled.png")
            if isfile(img_scaled_local):
                # user did not skip this image,
                remove(img_raw_local)
                rename(img_scaled_local, img_raw_local)

        # go to end screen
        screen.nextScreen({"pack_location": pack_location}, "manual")

# ran every time an option is changed in manualPage
def update_preview():
    global img_raw, img_scaled
    process_image(screen.get_args(), img_raw, img_scaled, scale_factor)

    screen.update_preview(img_raw, img_scaled)


def previous_image():
    global imageIndex
    imageIndex = imageIndex - 2
    initialize_next_image()


def open_scaled_image():
    global img_scaled
    startfile(img_scaled)

# Fixes directories of local files when compiled into auto-py-to-exe
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)
