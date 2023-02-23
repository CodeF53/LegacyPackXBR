# Libraries:
import os
import sys
import subprocess
import traceback

import numpy as np
from PIL import Image

# Custom Shit
import console_printing as cp


# processes image:
#   if it contains transparency, it scales alpha and RGB channels separately, upscales them, then merges them
#   otherwise, it upscales the image, then culls the transparency introduced by scaling
def process_image(input_path, output_path, image_name, scale_factor, algorithm):
  # I know this is fucking horrible, but I had to do it sometime.
  if image_name == "pack.png":
    return

  print(cp.ral(f"Processing {image_name}"))

  tile_image(input_path, image_name, 2)

  # make directory for shit to go in
  os.makedirs(output_path, exist_ok=True)

  if contains_transparency(input_path, image_name):
    # create strings for future readability
    image_name_alpha = image_name[0:-4] + "_alpha.png"
    image_name_rgb = image_name[0:-4] + "_rgb.png"
    # split image into alpha and rgb channels
    split_rgb_a(input_path, image_name, image_name_rgb, image_name_alpha)

    # upscale split images
    xbr(input_path, output_path, image_name_alpha, scale_factor, algorithm)
    xbr(input_path, output_path, image_name_rgb, scale_factor, algorithm)

    # merge upscaled image_name_alpha and image_name_color into image_name
    merge_rgb_a(output_path, image_name, image_name_rgb, image_name_alpha)

    # Cleanup
    os.remove(f"{output_path}{image_name_alpha}")
    os.remove(f"{output_path}{image_name_rgb}")
  else:
    # upscale image
    xbr(input_path, output_path, image_name, scale_factor, algorithm)

    # cull transparency from upscaled image
    cull_transparency(output_path, image_name)

  trim_tile(output_path, image_name, int(scale_factor) * 2)

  print(cp.ral(f"Finished {image_name}"))
  #cp.remove_line()


# wraps image with border_size pixel border of itself (like a tiled plane of the image)
def tile_image(path, image_name, border_size):
  img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()
  img_width, img_height = [len(img[0, :]), len(img)]

  # Protection for if the image is super small
  if img_width == 1 | img_height == 1:
    return

  # img[y,x]
  # vertical sandwich  bottom border_size lines -- image -- top border_size lines
  img = np.vstack([img[img_height - border_size:img_height, :], img, img[0:border_size, :]])

  # horizontal sandwich  right border_size lines -- image -- left border_size lines
  img = np.hstack([img[:, img_width - border_size:img_width], img, img[:, 0:border_size]])

  Image.fromarray(img).save(f"{path}{image_name}")


# trims num_pixels from all edges of input image
def trim_tile(path, image_name, num_pixels):
  img = np.asarray(Image.open(f"{path}{image_name}").convert('RGBA')).copy()
  img_width, img_height = [len(img[0, :]), len(img)]

  # Protection for if the image is super small
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
    # If the above fails, it means we aren't compiled, so paths work normally
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)


# TODO: linux
# Calls ScalerTest_Windows.exe with the proper args
def xbr(input_path, output_path, image_name, scale_factor, algorithm):
  try:
    arguments = f"-{scale_factor}{algorithm} \"{input_path}{image_name}\" \"{output_path}{image_name}\""
    subprocess.check_output(  # launch a process with args, pausing main thread until process is finished
      "ScalerTest_Windows.exe " +  # resource_path("ScalerTest_Windows.exe") +  # call in a way that works with files packed into an exe
      arguments,  # args for xBRz on our image
      creationflags=0x08000000)  # don't show the console window doing this.
  except Exception:
    traceback.print_exc()
    input(cp.ctr("press any key to exit"))
    exit()
