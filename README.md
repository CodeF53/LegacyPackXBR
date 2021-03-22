PackXBR
===========================
About:
-------------
This project is for the automation of the creation of Resource Packs for minecraft, implementing XBR scaling.

Usage:
-------------
Drop a ResourcePack zip onto PackXBR.exe

OR Open PackXBR.exe, press enter, then enter the path to a ResourcePack zip

Building
-------------
Requirements:
* a compiled windows [xbrzscale](https://github.com/atheros/xbrzscale) binary
* Python3
* Python3 libraries:
  * shutil
  * distutils
  * glob
  * zipfile
  * subprocess
* runtime `.dll`s for [SDL2](https://www.libsdl.org/download-2.0.php) and [SDL_image](https://www.libsdl.org/projects/SDL_image/)
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
* [Zenju's xBRz](https://sourceforge.net/projects/xbrz/)
  * A nice xBR modification
* [xBRzScale](https://github.com/atheros/xbrzscale)
  * A barebones implementation of xBRz
* Misterk7_-
  * Creator of VanillaXBR, a the pack that inspired this.
    * if you are interested enough to read to here, [you should join the discord](https://discord.gg/jruhHac)
