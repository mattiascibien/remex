import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter", "PIL","argparse"], "excludes": [], "icon": "NuvolaTileIcon.ico", "include_files":[("NuvolaTileIcon.ico","NuvolaTileIcon.ico")]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [ Executable("main.py",base="Console"), Executable("gui.py",base="Win32GUI") ]

setup(  name = "Remex",
        version = "0.1",
        description = "Remex is a set of tools to facilitate the use of RPG-Maker compatible graphics outside RPG Maker, in your own game engine",
        options = {"build_exe": build_exe_options},
        executables = executables)

