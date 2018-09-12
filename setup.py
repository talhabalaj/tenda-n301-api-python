import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tenda-n301-python-api",
    version="0.0.1",
    author="Talha Balaj",
    author_email="talhabalaj@gmail.com",
    description="Unofficial Tenda Model N301 Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talhabalaj/tenda-n301-api-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
)
