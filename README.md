PackXBR
===========================
About:
-------------
This project is for the automation of the creation of Resource Packs for minecraft, implementing XBR scaling.

Usage:
-------------
Drop a ResourcePack zip onto `PackXBR.exe` or `__main__.py`
OR
Open `PackXBR.exe` or `__main__.py`, press enter, then enter the path to a ResourcePack zip

Building
-------------
Requirements:
* Add [ScalarTest.exe](https://sourceforge.net/projects/xbrz/) to main folder
* Python3
* msvcrt
* shutil
* distutils
* glob
* zipfile
* subprocess
* Pillow (PIL fork)

Run `build.bat`

To-Do:
-------------
General:
* Create online utility
  * May require a python port of xBRz

PackXBR:
* Allow input of folders
* Improve output look
  * Modify `pack.mcmeta`
  * Have a set pack.png
* Location specific processing
  * Disable wrapping within `\assets\minecraft\textures\item`
  * Enable relayer masking within `\assets\minecraft\textures\entity`

ModPackXBR:
* Unpack `.jar` files
  * keep all in `textures`
  * remove folders without any images

Credits:
-------------
* [Zenju's xBRz and his ScalerTest binary](https://sourceforge.net/projects/xbrz/)
  *neat implementation of many scaling algorithms.
* Misterk7_-
  * Creator of VanillaXBR, a the pack that inspired this.
    * if you are interested enough to read to here, [you should join the discord](https://discord.gg/jruhHac)
