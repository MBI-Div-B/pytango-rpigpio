from setuptools import setup, find_packages

setup(
    name="rpigpio",
    version="0.0.1",
    description="tango device to control raspberry GPIO",
    author="Leonid Lunin",
    author_email="lunin.leonid@gmail.com",
    python_requires=">=3.6",
    entry_points={"console_scripts": ["RPiGPIO = tangods_rpigpio:main"]},
    license="MIT",
    packages=["tangods_rpigpio"],
    install_requires=[
        "pytango>=9.3.3",
        "RPi.GPIO>=0.7.0",
    ],
    url="https://github.com/lrlunin/pytango-moenchZmqServer",
    keywords=[
        "tango device",
        "tango",
        "pytango",
        "gpio",
    ],
)
