pyinstaller --onefile --collect-all TkinterDnD2 --windowed  ^
    --icon "packXBR.ico" --name "PackXBR" ^
    --add-data "ScalerTest_Windows.exe;." ^
    --add-data "tcl/*;tcl/" ^
    "main.py"

