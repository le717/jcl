from datetime import datetime
from cx_Freeze import setup, Executable


build_options = {"packages": [], "excludes": []}
base = "Console"
executables = [Executable("jcl.py", base=base)]

setup(
    name="jcl",
    version=datetime.now().strftime("%Y.%m.%d"),
    description="A tool for flashing Juniper EX switch configurations.",
    options={"build_exe": build_options},
    executables=executables,
)
