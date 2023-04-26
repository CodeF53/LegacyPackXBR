PackXBR
===========================
Archived in favor of [web-based version](https://github.com/CodeF53/WebPackXBR).

About:
-------------
This project is for the automation of the creation of Resource Packs for minecraft, implementing XBR scaling.

Usage:
-------------
Download https://sourceforge.net/projects/xbrz/ and put `ScalerTest_Windows.exe` into the same directory as `PackXBR.exe`

Drop a ResourcePack zip onto `PackXBR.exe`

OR Open `PackXBR.exe`, press enter, then enter the path to a ResourcePack zip

Tutorial video:

https://user-images.githubusercontent.com/37855219/165995159-6b8c2c81-4f74-4c7b-be39-377ad06bcea6.mp4

Building
-------------
Requirements:
* Python3
* Python3 libraries:
  * shutil
  * glob
  * zipfile
  * subprocess
  * webbrowser
* Pillow (PIL fork)

Run `build.bat`

To-Do:
-------------
General:
* Linux Support
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
  * A nice tool for comparing many scaling algorithms.
* Misterk7_-
  * Creator of VanillaXBR, the pack that inspired this.
  * if you are interested enough to read to here, [you should join the discord](https://discord.gg/8N4xzej)
