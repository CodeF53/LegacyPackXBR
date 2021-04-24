pyinstaller --onefile --console ^
    --icon "packXBR.ico" --name "PackXBR" ^
    --add-data "xbrzscale.exe;." ^
      --add-binary "SDL2_image.dll;." --add-binary "SDL2.dll;." ^
      --add-binary "libpng16-16.dll;." --add-binary "zlib1.dll;." ^
      --add-binary "libwinpthread-1.dll;." ^
    "main.py"

del  *.pyo PackXBR.spec
rmdir /Q /s __pycache__
rmdir /Q /s build

pause 
