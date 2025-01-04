from setuptools import setup, find_packages

setup(
    name="srt_textgrid_converter",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["srt_textgrid_converter"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "srt_textgrid_converter=srt_textgrid_converter:main",
        ],
    },
    author="Julian Vargo",
    author_email="julianvargo@berkeley.edu",
    description="Convert SRT files to TextGrids",
    url="https://github.com/julian-vargo/srt_textgrid_converter",
    classifiers=[
        "Programming Language :: Python :: 3.12.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
