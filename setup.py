from setuptools import setup, find_packages

setup(
    name="T_BAG",
    version="1.0.1",  # Update version number for each release
    packages=find_packages(),  # Automatically finds all packages and modules
    install_requires=[],
    entry_points={
        "console_scripts": [
            "T_BAG=T_BAG.main:main",
        ],
    },
    python_requires=">=3.6",  # Specify Python version compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Text-Based Adventure Game source code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Flameblade375/Text-based-Adventure-Game-Source-Code",
    author="Alexander.E.F",
    author_email="alexander@xandy.rocks",
    license="MIT",
)
