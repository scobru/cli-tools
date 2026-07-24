from setuptools import setup

setup(
    name="cryptomessage",
    version="1.0.0",
    description="End-to-End Encrypted Messaging (GUI & CLI)",
    py_modules=["cryptomessage", "cryptomessage_cli"],
    install_requires=["cryptography"],
    entry_points={
        "console_scripts": [
            "cryptomessage=cryptomessage:main",
            "cryptomessage-cli=cryptomessage_cli:main",
        ],
    },
)
