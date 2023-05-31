"""
Build executable file using pyisntaller
"""

import PyInstaller.__main__
import platform

# Edit these variables
# 16 bytes
app_encrypt_key = "MaZ1!-%!ls98A-2X"
app_name = "app_gui_template"
app_ico = "app.ico"

if platform.system() == "Windows":
    sep = ";"
else:
    sep = ":"
PyInstaller.__main__.run([
    "app_gui.py",
    "--onefile",
    f"--key={app_encrypt_key}",
    "--clean",
    "--noconsole",
    "--windowed",
    f"--name={app_name}",
    f"--icon=images/{app_ico}",
    f"--add-data=images/*{sep}images/"
])


# Command: pandoc README.md -s -o README.html
try:
    import pandoc
    md = pandoc.read(file="README.md", format="markdown")
    pandoc.write(doc=md, file="README.html", options=["-s"])
except:
    pass