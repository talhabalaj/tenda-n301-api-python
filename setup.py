import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tenda",
    version="0.0.8",
    author="Talha Balaj",
    author_email="talhabalaj@gmail.com",
    description="Unofficial Tenda Model N301 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talhabalaj/tenda-n301-api-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
