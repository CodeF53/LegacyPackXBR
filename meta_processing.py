# Libraries:
from PIL import Image


# root = "C:\Users\Chase\AppData\Roaming\.minecraft\resourcepacks\temp_aaa\assets\minecraft\textures"
# relative_location = "\block\"
# image_name = "grass.png"
def meta_process(root, relative_location, image_name):
    border = ""
    relayer = False
    alpha_scale = False
    alias = True

    transparency = contains_transparency(f"{root}{relative_location}", image_name)
    alpha_scale = transparency
    alias = not transparency

    # Fucking bullshit to assign each rel loc to a certain treatment

    return border, relayer, alpha_scale, alias


# goes through each pixel of the input image, testing if 0 < a < 255, returning true if that is the case
def contains_transparency(path, image_name):
    img = Image.open(f"{path}{image_name}").convert("RGBA")

    # for every pixel
    for x in range(img.width):
        for y in range(img.height):
            if 0 < img.getpixel((x, y))[3] < 255:  # if alpha channel is between 0 and 255
                return True

    return False
