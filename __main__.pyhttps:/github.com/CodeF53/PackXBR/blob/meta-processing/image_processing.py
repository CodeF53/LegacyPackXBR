# Libraries:
import os
import sys
import subprocess
import numpy as np
from PIL import Image

# Custom Shit
import console_printing as cp


# processes image:  process_image(input_path, output_path, image_name, border="empty", relayer=Boolean, alpha_scale=Boolean):
# Manages the processing of images pre and post upscale.
#       input_path      Full Directory pointing where image is stored
#       output_path     Full Directory pointing where processee image is to be saved
#       image_name      Name of image, including file extension
#
#       border      how the edges of the images should be treated during upscale
#           "empty"     extends borders and fills them transparently
#           "tile"      treats borders as if they were made of the original image tiled on a plane
#           "extend"    copies pixels from edge into borders
#       
#       relayer     Layers a Nearest-Neighbor Upscale under the Result
#           True/False
#
#   Perhaps alpha_scale would be better off as 2 seperate commands.
#       alpha_scale
#           True    Upscales RGB and Alpha Channels indivdually, then merges them back together
#           False   Upscales Regularly, then culls transparency created during upscale
def process_image(input_path, output_path, image_name, border="empty", relayer=False, alpha_scale=False):
    # would've used a switch here, but python doesnt have them
    if border == "empty":
        border_empty(input_path, image_name, 2)
    elif border == "tile":
        border_tile(input_path, image_name, 2)
    elif border == "extend":
        border_extend(input_path, image_name, 2)

    # Upscales RGB and Alpha Channels indivdually, then merges them back together
    if alpha_scale:
        # split image into RGB and A
        image_name_alpha = image_name[0:-4] + "_alpha.png"
        image_name_rgb = image_name[0:-4] + "_rgb.png"
        split_rgb_a(input_path, image_name, image_name_rgb, image_name_alpha)

        # upscale RGB and A separately
        xbr_4x(input_path, output_path, image_name_alpha)
        xbr_4x(input_path, output_path, image_name_rgb)

        # merge upscaled RGB and A back into RGBA
        merge_rgb_a(output_path, image_name, image_name_rgb, image_name_alpha)

        # remove temporary files
        os.remove(f"{output_path}{image_name_alpha}")
        os.remove(f"{output_path}{image_name_rgb}")
    # Upscales Regularly, then culls transparency created during upscale
    else:
        # upscale image
        xbr_4x(input_path, output_path, image_name)

        # cull transparency created during upscale
        cull_transparency(output_path, image_name)
        cp.remove_lines(5)

    # Layers a Nearest-Neighbor Upscale under the Result
    if relayer:
        # do stuff
        print("Tell CodeF53 to implement relayering")

    # Crops into the outputted image 8 pixels on all sides, getting rid of border bullshit
    trim_border(output_path, image_name, 8)


# copies pixels from outermost edges outwards
def border_extend(path, image_name, border_size):
    img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()

    # Temporary Protection for if the image is super small,
    #    Replace with Meta-Processing later on
    img_width, img_height = [len(img[0, :]), len(img)]
    if img_width == 1 | img_height == 1:
        return

    for i in range(border_size):
        img_width, img_height = [len(img[0, :]), len(img)]
        img = np.vstack([
            img[0:1, :],
            img,
            img[img_height - 1:img_height, :]])

        img = np.hstack([
            img[:, 0:1],
            img,
            img[:, img_width - 1:img_width]])

    Image.fromarray(img).save(f"{path}{image_name}")


# wraps image with transparent pixel border
def border_empty(path, image_name, border_size):
    img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()
    img_width, img_height = [len(img[0, :]), len(img)]

    # Temporary Protection for if the image is super small,
    #    Replace with Meta-Processing later on
    if img_width == 1 | img_height == 1:
        return

    # img[y,x]
    img = np.vstack([
        np.zeros((border_size, img_height, 4), dtype=np.uint8),
        img,
        np.zeros((border_size, img_height, 4), dtype=np.uint8)])

    # horizontal sandwich  right border_size lines -- image -- left border_size lines
    img = np.hstack([
        np.zeros((img_width + 2 * border_size, border_size, 4), dtype=np.uint8),
        img,
        np.zeros((img_width + 2 * border_size, border_size, 4), dtype=np.uint8)])

    Image.fromarray(img).save(f"{path}{image_name}")


# wraps image with border as if it was a tile on a plane of itself
def border_tile(path, image_name, border_size):
    img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()
    img_width, img_height = [len(img[0, :]), len(img)]

    # Temporary Protection for if the image is super small,
    #    Replace with Meta-Processing later on
    if img_width == 1 | img_height == 1:
        return

    # img[y,x]
    # vertical sandwich  bottom border_size lines -- image -- top border_size lines
    img = np.vstack([img[img_height - border_size:img_height, :], img, img[0:border_size, :]])

    # horizontal sandwich  right border_size lines -- image -- left border_size lines
    img = np.hstack([img[:, img_width - border_size:img_width], img, img[:, 0:border_size]])

    Image.fromarray(img).save(f"{path}{image_name}")


# trims num_pixels from all edges of input image
def trim_border(path, image_name, num_pixels):
    img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()
    img_width, img_height = [len(img[0, :]), len(img)]

    # Temporary Protection for if the image is super small,
    #    When meta-processing is added, this will be unnecessary
    if img_width == 1 | img_height == 1:
        return

    img = img[num_pixels:img_height - num_pixels, num_pixels:img_width - num_pixels]

    Image.fromarray(img).save(f"{path}{image_name}")


# splits image into rgb and alpha channels, saving under image_name_rgb and image_name_alpha
def split_rgb_a(path, image_name, image_name_rgb, image_name_alpha):
    img = Image.open(f"{path}{image_name}").convert("RGBA")
    img_rgb = img.convert("RGB")
    img_alpha = img.convert("RGB")

    # for every pixel, take the alpha value from img, and set img_alpha's rgb channels to equal said alpha
    for x in range(img.width):
        for y in range(img.height):
            alpha = img.getpixel((x, y))[3]
            img_alpha.putpixel((x, y), (alpha, alpha, alpha))

    img_rgb.save(f"{path}{image_name_rgb}")
    img_alpha.save(f"{path}{image_name_alpha}")


# merges rgb and alpha into image_name
def merge_rgb_a(path, image_name, image_name_rgb, image_name_alpha):
    img = Image.open(f"{path}{image_name_rgb}").convert("RGBA")
    img_alpha = Image.open(f"{path}{image_name_alpha}").convert("RGB")

    for x in range(img.width):
        for y in range(img.height):
            alpha = img_alpha.getpixel((x, y))[0]
            img.putpixel((x, y), img.getpixel((x, y))[:3] + (alpha,))

    img.save(f"{path}{image_name}")


# goes through each pixel of the input image, testing if 0 < a < 255, returning true if that is the case
def contains_transparency(path, image_name):
    img = Image.open(f"{path}{image_name}").convert("RGBA")

    # for every pixel
    for x in range(img.width):
        for y in range(img.height):
            if 0 < img.getpixel((x, y))[3] < 255:  # if alpha channel is between 0 and 255
                return True

    return False


# goes through each pixel of the input image, testing if 0 < a < 255, setting it to 0 if that is the case
def cull_transparency(path, image_name):
    img = Image.open(f"{path}{image_name}").convert("RGBA")

    # for every pixel
    for x in range(img.width):
        for y in range(img.height):
            if 0 < img.getpixel((x, y))[3] < 255:  # if alpha channel is between 0 and 255
                img.putpixel((x, y), (0, 0, 0, 0))

    img.save(f"{path}{image_name}")


# Fixes directories of local files when compiled into auto-py-to-exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyUnresolvedReferences
        base_path = sys._MEIPASS
    except Exception:
        # If the above fails, it means we arent compiled, so paths work normally
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Calls xbrzscale.exe with the proper args
def xbr_4x(input_path, output_path, image_name):
    arguments = f"4 \"{input_path}{image_name}\" \"{output_path}{image_name}\""
    subprocess.check_output(  # launch a process with args, pausing main thread until process is finished
        resource_path("xbrzscale.exe ") +  # call in a way that works with files packed into an exe
        arguments,  # args for 4x xBRz on our image
        creationflags=0x08000000)  # don't show the console window doing this.
