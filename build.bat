pyinstaller --onefile --console ^
  --icon "packXBR.ico" --name "PackXBR" ^
  "main.py"

del  *.pyo PackXBR.spec
rmdir /Q /s __pycache__
rmdir /Q /s build

pause
