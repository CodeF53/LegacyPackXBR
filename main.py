# libraries
import sys
from shutil import rmtree
from shutil import copytree
import os
import glob
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
from os.path import exists
from webbrowser import open as openurl

# custom shit
from image_processing import process_image
import file_processing as fp
import console_printing as cp


# asks for a ResourcePack zip until it gets a valid zip file
# returns root, (zip_)name
def user_input_zip(user_input):
    zip_exists, root_tmp, name_tmp, extension = fp.file_meta(user_input)
    if not zip_exists:
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
    cp.remove_lines(4)
    print("")
    return root_tmp, name_tmp


# asks for a Scale Factor until it gets a valid scale factor
def user_input_scale_factor(user_input):
    if user_input != "2" and user_input != "4" and user_input != "6":
        cp.remove_lines(5)
        os.system('')
        print("\n" + cp.text["RED--"] + cp.ctr("invalid scale factor") + cp.text["NORM-"])
        os.system('')
        return user_input_scale_factor(input(cp.ctr("scale images by what factor? (2, 4, or 6)") + "\n\n" + cp.text["GREEN"]))
    cp.remove_lines(4)
    print("")
    return user_input

def user_input_algorithm(user_input):
    if user_input != "xBR" and user_input != "xBRZ":
        cp.remove_lines(10)
        os.system('')
        print("\n" + cp.text["RED--"] + cp.ctr("invalid algorithm") + cp.text["NORM-"])
        os.system('')

        print(cp.text['NORM-'] + cp.ctr("What scaling algorithm do you want to use? (xBR or xBRZ)"))
        print("\nxBR  - Used for organic visuals, like the patterns on grass or leaves."
              "\n\tSmooths things out a lot more, blending a lot of color and geometry.")
        print("xBRZ - Used for sharper visuals, like the sharper edges of a brick texture."
              "\n\tBlends less colors together, staying closer to the source texture.")
        return user_input_algorithm(input("\n" + cp.text["GREEN"]))
    cp.remove_lines(9)
    print("")
    return user_input

def main():
    os.system('')
    print(cp.ctrs(" _____           _    __   ______  _____  ", f"{cp.text['CYAN-']} _____           _    {cp.text['BLUE-']}__   ______  _____  {cp.text['NORM-']}"))
    print(cp.ctrs("|  __ \\CodeF53's| |   \\ \\ / /  _ \\|  __ \\ ", f"{cp.text['CYAN-']}|  __ \\{cp.text['BLUE-']}CodeF53's{cp.text['CYAN-']}| |   {cp.text['BLUE-']}\\ \\ "f"/ /  _ \\|  __ \\ {cp.text['NORM-']}"))
    print(cp.ctrs("| |__) |_ _  ___| | __ \\ V /| |_) | |__) |", f"{cp.text['CYAN-']}| |__) |_ _  ___| | __ {cp.text['BLUE-']}\\ V /| |_) | |__) |{cp.text['NORM-']}"))
    print(cp.ctrs("|  ___/ _` |/ __| |/ /  > < |  _ <|  _  / ", f"{cp.text['CYAN-']}|  ___/ _` |/ __| |/ /  {cp.text['BLUE-']}> < |  _ <|  _  / {cp.text['NORM-']}"))
    print(cp.ctrs("| |  | (_| | (__|   <  / . \\| |_) | | \\ \\ ", f"{cp.text['CYAN-']}| |  | (_| | (__|   <  {cp.text['BLUE-']}/ . \\| |_) | | \\ \\ {cp.text['NORM-']}"))
    print(cp.ctrs("|_|   \\__,_|\\___|_|\\_\\/_/ \\_\\____/|_|  \\_\\", f"{cp.text['CYAN-']}|_|   \\__,_|\\___|_|\\_\\{cp.text['BLUE-']}/_/ \\_\\____/|_|  \\_\\{cp.text['NORM-']}"))
    print("\n")

    # Check if there is a valid ScalarTest binary in the same directory as PackXBR
    # TODO: figure out how linux works with binaries, do we need to add executable args with chmod ourselves?
    if not (exists("ScalerTest_Windows.exe")):  # or exists("ScalerTest_Linux")):
        # complain and point user in right direction
        openurl("https://sourceforge.net/projects/xbrz/files/latest/download")
        print(cp.text["RED--"] + cp.ctr("PackXBR requires ScalarTest in the same directory as itself"))
        input(cp.text['NORM-'] + cp.ctr("press any key to exit"))
        exit()

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

    # ask about what scale they want
    scale_factor = user_input_scale_factor(
        input(cp.text['NORM-'] + cp.ctr("scale images by what factor? (2, 4, or 6 (xBRZ only))") + "\n\n" + cp.text["GREEN"]))

    # ask what algorithm to use
    if scale_factor == "6":
        print(cp.text['RED--'] + cp.ctr("scale factor is set to 6, which is only supported by xBRZ") +
              cp.text['NORM-'] + cp.ctr("Defaulting to xBRZ algorithm...") + "\n")
        algorithm = "xBRZ"
    else:
        print(cp.text['NORM-'] + cp.ctr("What scaling algorithm do you want to use? (xBR or xBRZ)"))
        print("\nxBR  - Used for organic visuals, like the patterns on grass or leaves."
              "\n\tSmooths things out a lot more, blending a lot of color and geometry.\n\n"
              "xBRZ - Used for sharper visuals, like the sharper edges of a brick texture."
              "\n\tBlends less colors together, staying closer to the source texture.")
        algorithm = user_input_algorithm(input("\n" + cp.text["GREEN"]))

    # unzip pack
    print(cp.text["NORM-"] + cp.ctr("unpacking zip to temporary folder"))
    fp.unzip(f"{root}{packName}.zip", f"{root}temp_{packName}")
    cp.remove_line()

    # copy files into final folder
    print(cp.ctr("moving non-image files from temporary folder to final pack") + "\n")
    copytree(f"{root}temp_{packName}", f"{root}XBR {packName}")
    cp.remove_lines(2)

    # overwrite images in final folder with processed images from temp folder
    print(cp.ctr("Processing all images:"))
    images = [y for x in os.walk(f"{root}temp_{packName}") for y in glob.glob(os.path.join(x[0], '*.png'))]
    totalImages = len(images)

    with ProcessPoolExecutor(max_workers=int(round((os.cpu_count()/4)*3, 0))) as executor:
        for i in range(totalImages):
            file_name = images[i][images[i].rfind("\\") + 1:]
            input_path = images[i][:images[i].rfind("\\") + 1]
            output_path = input_path.replace(f"temp_{packName}", f"XBR {packName}")

            executor.submit(process_image, input_path=input_path, output_path=output_path, image_name=file_name, scale_factor=scale_factor, algorithm = algorithm)

    # clean up
    print("\n" + cp.ctr("removing temporary files"))
    rmtree(f"{root}temp_{packName}")
    cp.remove_line()

    print("\n\n" + cp.ctr("Done!"))
    input(cp.ctr("press any key to exit"))


if __name__ == '__main__':
    freeze_support()
    main()
