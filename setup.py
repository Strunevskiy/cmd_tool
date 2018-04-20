from setuptools import setup, find_packages

setup(
    name="coffee for me",
    version="0.1.0",
    author="Aleh Struneuski",
    author_email="oleg.strunevskiy@gmail.com",
    packages=find_packages(),
    install_requires=["pymysql", "six", "future", "mock"]
)
