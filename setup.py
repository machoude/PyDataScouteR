from setuptools import setup, find_packages

setup(
    name="pydatascouteR",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.5.0",
    ],
)