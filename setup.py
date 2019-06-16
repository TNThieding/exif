import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    install_requires=[
        'enum34',
        ],
    include_package_data=True,

    name='exif',
    version='0.6.0',
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
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Editors',
        ],
    license='MIT License',
    packages=setuptools.find_packages()
)