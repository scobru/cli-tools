from setuptools import setup

setup(
    name="opass",
    version="1.0.0",
    description="Organic Password Generator CLI",
    py_modules=["opass"],
    entry_points={
        "console_scripts": [
            "opass=opass:main",
        ],
    },
)
