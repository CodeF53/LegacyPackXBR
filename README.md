PackXBR
===========================
About:
-------------
This project is for the automation of the creation of Resource Packs for minecraft, implementing XBR scaling.

To-Do:
-------------
General:
* Create online utility
* Switch to XBRz in 2D-ImageFilter
* Multithreading
* Optimize Image Processing:
 * contains_transparency()
 * split_rgb_a()
 * merge_rgb_a()
 * cull_transparency()

PackXBR:
* Modify pack.mcmeta
* Have a set pack.png
* Enable relayer masking when processing textures within `\assets\minecraft\textures\entity`

ModPackXBR (not yet created):
* Unpack .jar files
  * somehow sort through what non image files need to be kept

Credits:
-------------
* [2D-ImageFilter](https://github.com/Hawkynt/2dimagefilter)
  * A utility for scaling algorithms with some great command-line integration

Prerequisites
-------------
* I have yet to figure these out, if it doesnt work for you:
  * Try to install python 3.0
