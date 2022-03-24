from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="ebbe",
    version="1.8.0",
    description="A collection of iterator-related functions for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/Yomguithereal/ebbe",
    license="MIT",
    author="Guillaume Plique",
    author_email="kropotkinepiotr@gmail.com",
    keywords="iter",
    python_requires=">=3.5",
    packages=find_packages(exclude=["test"]),
    package_data={"docs": ["README.md"]},
    install_requires=[],
    zip_safe=True,
)
