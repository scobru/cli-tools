from setuptools import setup

setup(
    name="cryptoclip",
    version="1.0.0",
    description="Clipboard Monitor and Fernet Encryption CLI",
    py_modules=["cryptoclip"],
    install_requires=["cryptography", "pyperclip", "pynput", "pystray", "Pillow"],
    entry_points={
        "console_scripts": [
            "cryptoclip=cryptoclip:main",
        ],
    },
)
