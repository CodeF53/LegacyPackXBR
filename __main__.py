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

text = {
    "RED--": u"\u001b[31m",
    "GREEN": u"\u001b[32m",
    "NORM-": u"\u001b[0m",
    "CYAN-": u"\u001b[36m",
    "BLUE-": u"\u001b[34m"
}


# asks for a ResourcePack zip until it gets a valid zip file
# returns root, (zip_)name
def user_input_zip(user_input):
    exists, root_tmp, name_tmp, extension = fp.file_meta(user_input)
    if not exists:
        cp.remove_lines(5)
        os.system('')
        print("\n" + text["RED--"] + cp.ctr("the file you entered either doesn't exist, or has an invalid path") + text[
            "NORM-"])
        os.system('')
        return user_input_zip(
            input(cp.ctr("please enter the full path to a ResourcePack zip file") + "\n\n" + text["GREEN"]))
    elif extension != ".zip":
        cp.remove_lines(5)
        os.system('')
        print("\n" + text["RED--"] + cp.ctr("the file you entered is not a zip") + text["NORM-"])
        os.system('')
        return user_input_zip(
            input(cp.ctr("please enter the full path to a ResourcePack zip file") + "\n\n" + text["GREEN"]))
    return root_tmp, name_tmp


os.system('')
print(cp.ctrs(" _____           _    __   ______  _____  ", f"{text['CYAN-']} _____           _    {text['BLUE-']}__   ______  _____  {text['NORM-']}"))
print(cp.ctrs("|  __ \\CodeF53's| |   \\ \\ / /  _ \\|  __ \\ ", f"{text['CYAN-']}|  __ \\{text['BLUE-']}CodeF53's{text['CYAN-']}| |   {text['BLUE-']}\\ \\ / /  _ \\|  __ \\ {text['NORM-']}"))
print(cp.ctrs("| |__) |_ _  ___| | __ \\ V /| |_) | |__) |", f"{text['CYAN-']}| |__) |_ _  ___| | __ {text['BLUE-']}\\ V /| |_) | |__) |{text['NORM-']}"))
print(cp.ctrs("|  ___/ _` |/ __| |/ /  > < |  _ <|  _  / ", f"{text['CYAN-']}|  ___/ _` |/ __| |/ /  {text['BLUE-']}> < |  _ <|  _  / {text['NORM-']}"))
print(cp.ctrs("| |  | (_| | (__|   <  / . \\| |_) | | \\ \\ ", f"{text['CYAN-']}| |  | (_| | (__|   <  {text['BLUE-']}/ . \\| |_) | | \\ \\ {text['NORM-']}"))
print(cp.ctrs("|_|   \\__,_|\\___|_|\\_\\/_/ \\_\\____/|_|  \\_\\", f"{text['CYAN-']}|_|   \\__,_|\\___|_|\\_\\{text['BLUE-']}/_/ \\_\\____/|_|  \\_\\{text['NORM-']}"))
print("\n")

# Get pack information
root = None
packName = None

# dropped file compatibility
if len(sys.argv) >= 2:
    os.system('')
    print(cp.ctr("please input the full path to a ResourcePack zip")+"\n")
    os.system('')
    print(text["GREEN"] + sys.argv[1])
    root, packName = user_input_zip(sys.argv[1])
else:
    os.system('')
    root, packName = user_input_zip(
        input(cp.ctr("please input the full path to a ResourcePack zip") + "\n\n" + text["GREEN"]))

# unzip pack
print("\n" + text["NORM-"] + cp.ctr("unpacking zip to temporary folder"))
fp.unzip(f"{root}{packName}.zip", f"{root}temp")

# copy files into final folder
print(cp.ctr("moving non-image files from temporary folder to final pack") + "\n")
copy_tree(f"{root}temp", f"{root}{packName}_xbr", update=1)

# overwrite images in final folder with processed images from temp folder
print(cp.ctr("Processing all images:"))
images = [y for x in os.walk(f"{root}temp") for y in glob.glob(os.path.join(x[0], '*.png'))]
totalImages = len(images)

for i in range(totalImages):
    cp.print_progress_bar(i, totalImages, prefix="", suffix="Complete", length=25)

    file_name = images[i][images[i].rfind("\\") + 1:]
    input_path = images[i][:images[i].rfind("\\") + 1]
    output_path = input_path.replace("temp", f"{packName}_xbr")

    process_image(input_path, output_path, file_name)
    cp.remove_lines(2)
cp.print_progress_bar(totalImages, totalImages, prefix="", suffix="Complete", length=25)

# clean up
print("\n" + cp.ctr("removing temporary files"))
rmtree(f"{root}temp")

print("\n\n" + cp.ctr("Done!"))
print(cp.ctr("press any key to exit"))
msvcrt.getch()
