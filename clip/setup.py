from setuptools import setup

setup(
    name="clip",
    version="1.0.0",
    description="Advanced Clipboard Manager CLI",
    py_modules=["clip"],
    install_requires=["pyperclip"],
    entry_points={
        "console_scripts": [
            "clipmgr=clip:main",
            "clip-tool=clip:main",
            "clip=clip:main",
        ],
    },
)
