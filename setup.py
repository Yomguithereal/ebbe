from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="ebbe",
    version="1.13.0",
    description="Collection of typical helper functions for python.",
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
    extras_require={
        ":python_version<'3.8'": ["typing_extensions"],
    },
    zip_safe=True,
)
