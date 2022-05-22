from shutil import copytree, copy
from zipfile import ZipFile
from os.path import isfile, join
from os import walk, rename, remove
from glob import glob

from image_processing import process_image

packLocation = ""
scale_factor = 4
imageLocations = []
imageIndex = 0

img_raw = ""
img_scaled = ""

screen = None


# Preps for upscaling
# - caches scale factor, pack location from args
# - unzips/clones to output directory -> "{packLocation}_xbr"
# - generates imageLocations
def initLogic(args, ManualGUI):
    global screen
    screen = ManualGUI
    # cache scale factor, pack location
    global packLocation, scale_factor, imageLocations
    packLocation = args.get("packLocation")
    scale_factor = args.get("scaleFactor")

    # unzip/clone to output directory -> "{packLocation}_xbr"
    if isfile(packLocation):
        # unzip to output directory
        ZipFile(packLocation, 'r').extractall(args.get("packLocation")[0:-4] + "_xbr")
        packLocation = packLocation[0:-4] + "_xbr"
    else:
        # clone to output directory
        copytree(src=packLocation, dst=packLocation + "_xbr")
        packLocation = packLocation + "_xbr"

    # generate list of locations to images
    # todo: make list go in a logical order, one folder then the next.
    imageLocations = [y for x in walk(packLocation) for y in glob(join(x[0], '*.png'))]

    # sdrnigthfuor
    initializeNextImage()

# deletes raw image and uses scaled image
# iterates imageIndex
def nextImage():
    global imageIndex, img_raw, img_scaled
    # put scaled image into place of raw image
    rename(img_scaled, img_raw)

    imageIndex = imageIndex + 1
    initializeNextImage()

# deletes scaled image and uses raw image
# iterates imageIndex
def skipImage():
    global imageIndex, img_scaled
    # delete scaled image
    remove(img_scaled)

    imageIndex = imageIndex + 1
    initializeNextImage()

# updates internal image variables
# ran by nextImage() and skipImage()
def initializeNextImage():
    global imageLocations, imageIndex
    global img_raw, img_scaled
    img_raw = imageLocations[imageIndex]

    img_scaled = img_raw.replace(".png", "_scaled.png")
    copy(img_raw, img_scaled)

    update_preview()

# ran every time an option is changed in manualPage
def update_preview():
    global img_raw, img_scaled
    process_image(screen.getArgs(), img_raw, img_scaled, scale_factor)

    screen.update_preview(img_raw, img_scaled)

