# Libraries:
import os
import sys
import subprocess
from PIL import Image

# Custom Shit
import console_printing as cp


# processes image:
#   if it contains transparency, it scales alpha and RGB channels separately, upscales them, then merges them
#   otherwise, it upscales the image, then culls the transparency introduced by scaling
def process_image(input_path, output_path, image_name):
    print(cp.ral(f"{image_name}"))

    # make directory for shit to go in
    os.makedirs(output_path, exist_ok=True)

    print(cp.ral("evaluating transparency        "))
    if contains_transparency(input_path, image_name):
        print(cp.ral("splitting image        "))
        # create strings for future readability
        image_name_alpha = image_name[0:-4] + "_alpha.png"
        image_name_rgb = image_name[0:-4] + "_rgb.png"
        # split image into alpha and rgb channels
        split_rgb_a(input_path, image_name, image_name_rgb, image_name_alpha)

        print(cp.ral("scaling channels        "))
        # upscale split images
        xbr_4x(input_path, output_path, image_name_alpha)
        xbr_4x(input_path, output_path, image_name_rgb)

        print(cp.ral("merging channels        "))
        # merge upscaled image_name_alpha and image_name_color into image_name
        merge_rgb_a(output_path, image_name, image_name_rgb, image_name_alpha)

        print(cp.ral("removing temp files        "))
        # Cleanup
        os.remove(f"{output_path}{image_name_alpha}")
        os.remove(f"{output_path}{image_name_rgb}")
        cp.remove_lines(6)
    else:
        print(cp.ral("scaling image        "))
        # upscale image
        xbr_4x(input_path, output_path, image_name)

        print(cp.ral("culling transparency        "))
        # cull transparency from upscaled image
        cull_transparency(output_path, image_name)
        cp.remove_lines(4)


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


# Calls ImageResizer.exe with the proper args
def xbr_4x(input_path, output_path, image_name):
    arguments = f"/load \"{input_path}{image_name}\" /resize auto \"XBR 4x(1, thresholds=1, hbounds=wrap, vbounds=wrap)\" /save \"{output_path}{image_name}\" "
    subprocess.check_output(  # launch a process with args, pausing main thread until process is finished
        resource_path("ImageResizer.exe ") +  # call in a way that works with files packed into an exe
        arguments,  # args for 4x vertically and horizontally wrapped, XBR
        creationflags=0x08000000)  # don't show the console window doing this.
