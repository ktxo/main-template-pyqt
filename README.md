
# Basic template for PyQt6 application

Basic template for PyQt6 python application 

----

# What is is this?
Just a *simple* skeleton for a PyQt6 application, including:

- Simple skeleton for app
- Some widgets
- [Build a single executable file](#build-executable) (pyinstaller)


## How to use

- Clone sources 
```
# "myapp" application
git clone git@github.com:ktxo/main-template-pyqt myapp
```

- Add your code to [app_gui.py](app_gui.py)
- Add your images to folder [images](images)
- Create a conda / virtualenv and install dependencies, see [requirements.txt](requirements.txt)
- Edit [_about.py](_about.py)
- Edit file [build_exe.py](build_exe.py) (see "Edit these variables")
- Build binary file:
```
python build_exe.py
```

Output in **dist** folder

