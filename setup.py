from cx_Freeze import setup, Executable 
base = None
executables = [Executable("app.py", base = "Win32GUI")] #Только для win

packages=["idna"]
options={
    'build.exe':{
        'packages':packages,
    },
}

setup(

name = "app",
options = options,
version = "1.1.1",
description = "ne trogat'",
executables = executables
)