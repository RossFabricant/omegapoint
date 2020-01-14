import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omegapoint",
    version="0.0.1",
    author="Ross Fabricant",
    description="Omega Point API Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RossFabricant/omega-point",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
