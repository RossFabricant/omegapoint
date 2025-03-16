import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omegapoint",
    version="0.0.4",
    scripts=[],
    author="Ross Fabricant",
    description="Omega Point API Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RossFabricant/omegapoint",
    packages=['omegapoint'],
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
        'requests>=2.25.0',
        'sgqlc>=9.1'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=2.12.0',
            'mypy>=0.910',
            'twine>=1.13.0'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
