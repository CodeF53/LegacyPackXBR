# libraries
import msvcrt
import sys
from shutil import rmtree
from distutils.dir_util import copy_tree
import os
import glob

# custom shit
from image_processing import process_image
import file_processing as fp
import console_printing as cp


# asks for a ResourcePack zip until it gets a valid zip file
# returns root, (zip_)name
def user_input_zip(user_input):
    exists, root_tmp, name_tmp, extension = fp.file_meta(user_input)
    if not exists:
        cp.remove_lines(5)
        os.system('')
        print("\n" + cp.text["RED--"] + cp.ctr("the file you entered either doesn't exist, or has an invalid path") +
              cp.text[
                  "NORM-"])
        os.system('')
        return user_input_zip(
            input(cp.ctr("please enter the full path to a ResourcePack zip file") + "\n\n" + cp.text["GREEN"]))
    elif extension != ".zip":
        cp.remove_lines(5)
        os.system('')
        print("\n" + cp.text["RED--"] + cp.ctr("the file you entered is not a zip") + cp.text["NORM-"])
        os.system('')
        return user_input_zip(
            input(cp.ctr("please enter the full path to a ResourcePack zip file") + "\n\n" + cp.text["GREEN"]))
    return root_tmp, name_tmp


os.system('')
print(cp.ctrs(" _____           _    __   ______  _____  ",
              f"{cp.text['CYAN-']} _____           _    {cp.text['BLUE-']}__   ______  _____  {cp.text['NORM-']}"))
print(cp.ctrs("|  __ \\CodeF53's| |   \\ \\ / /  _ \\|  __ \\ ",
              f"{cp.text['CYAN-']}|  __ \\{cp.text['BLUE-']}CodeF53's{cp.text['CYAN-']}| |   {cp.text['BLUE-']}\\ \\ "
              f"/ /  _ \\|  __ \\ {cp.text['NORM-']}"))
print(cp.ctrs("| |__) |_ _  ___| | __ \\ V /| |_) | |__) |",
              f"{cp.text['CYAN-']}| |__) |_ _  ___| | __ {cp.text['BLUE-']}\\ V /| |_) | |__) |{cp.text['NORM-']}"))
print(cp.ctrs("|  ___/ _` |/ __| |/ /  > < |  _ <|  _  / ",
              f"{cp.text['CYAN-']}|  ___/ _` |/ __| |/ /  {cp.text['BLUE-']}> < |  _ <|  _  / {cp.text['NORM-']}"))
print(cp.ctrs("| |  | (_| | (__|   <  / . \\| |_) | | \\ \\ ",
              f"{cp.text['CYAN-']}| |  | (_| | (__|   <  {cp.text['BLUE-']}/ . \\| |_) | | \\ \\ {cp.text['NORM-']}"))
print(cp.ctrs("|_|   \\__,_|\\___|_|\\_\\/_/ \\_\\____/|_|  \\_\\",
              f"{cp.text['CYAN-']}|_|   \\__,_|\\___|_|\\_\\{cp.text['BLUE-']}/_/ \\_\\____/|_|  \\_\\{cp.text['NORM-']}"))
print("\n")


# Get pack information
root = None
packName = None


# dropped file compatibility
if len(sys.argv) >= 2:
    os.system('')
    print(cp.ctr("please input the full path to a ResourcePack zip") + "\n")
    os.system('')
    print(cp.text["GREEN"] + sys.argv[1])
    root, packName = user_input_zip(sys.argv[1])
else:
    os.system('')
    root, packName = user_input_zip(
        input(cp.ctr("please input the full path to a ResourcePack zip") + "\n\n" + cp.text["GREEN"]))

# unzip pack
print("\n" + cp.text["NORM-"] + cp.ctr("unpacking zip to temporary folder"))
fp.unzip(f"{root}{packName}.zip", f"{root}temp_{packName}")

# copy files into final folder
print(cp.ctr("moving non-image files from temporary folder to final pack") + "\n")
copy_tree(f"{root}temp_{packName}", f"{root}XBR {packName}", update=1)

# overwrite images in final folder with processed images from temp folder
print(cp.ctr("Processing all images:"))
images = [y for x in os.walk(f"{root}temp_{packName}") for y in glob.glob(os.path.join(x[0], '*.png'))]
totalImages = len(images)

for i in range(totalImages):
    cp.print_progress_bar(i, totalImages, prefix="", suffix="Complete", length=25)

    file_name = images[i][images[i].rfind("\\") + 1:]
    input_path = images[i][:images[i].rfind("\\") + 1]
    output_path = input_path.replace(f"temp_{packName}", f"XBR {packName}")

    process_image(input_path, output_path, file_name)
    cp.remove_lines(2)
cp.print_progress_bar(totalImages, totalImages, prefix="", suffix="Complete", length=25)

# clean up
print("\n" + cp.ctr("removing temporary files"))
rmtree(f"{root}temp_{packName}")

print("\n\n" + cp.ctr("Done!"))
print(cp.ctr("press any key to exit"))
msvcrt.getch()
