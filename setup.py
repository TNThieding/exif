import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    version = fh.read()

setuptools.setup(
    python_requires='>=3.5',
    include_package_data=True,

    name='exif',
    version=version,
    author='Tyler N. Thieding',
    author_email='python@thieding.com',
    maintainer='Tyler N. Thieding',
    maintainer_email = 'python@thieding.com',
    url='https://github.com/TNThieding/exif',
    description='Read and modify image EXIF metadata using Python.',
    long_description=long_description,
    download_url='https://github.com/TNThieding/exif',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Graphics :: Editors',
        ],
    license='MIT License',
    packages=setuptools.find_packages()
)
