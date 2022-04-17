from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    version = fh.read()

setup(
    python_requires=">=3.7",
    install_requires=[
        "plum-py>=0.5.0,<2.0.0",
    ],
    include_package_data=True,
    name="exif",
    version=version,
    author="Tyler N. Thieding",
    author_email="python@thieding.com",
    maintainer="Tyler N. Thieding",
    maintainer_email="python@thieding.com",
    url="https://gitlab.com/TNThieding/exif",
    description="Read and modify image EXIF metadata using Python.",
    long_description=long_description,
    download_url="https://gitlab.com/TNThieding/exif",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Graphics :: Editors",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
)
