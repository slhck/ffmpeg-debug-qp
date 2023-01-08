import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Versioning
with open(os.path.join(here, "ffmpeg_debug_qp_parser", "__init__.py")) as version_file:
    for line in version_file:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ffmpeg_debug_qp_parser",
    version=version,
    description="Extract QP values of input video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slhck/ffmpeg-debug-qp",
    author="Werner Robitza",
    author_email="werner.robitza@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    packages=["ffmpeg_debug_qp_parser"],
    entry_points={
        "console_scripts": [
            "ffmpeg-debug-qp-parser=ffmpeg_debug_qp_parser.__main__:main",
        ],
    },
)
