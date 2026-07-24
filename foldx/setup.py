from setuptools import setup

setup(
    name="foldx",
    version="1.0.0",
    description="Folder Organizer CLI",
    py_modules=["foldx"],
    entry_points={
        "console_scripts": [
            "foldx=foldx:organizza_cartella",
        ],
    },
)
