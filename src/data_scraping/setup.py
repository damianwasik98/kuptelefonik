from typing import List
from setuptools import find_packages, setup

def get_requirements() -> List[str]:
    return [x.strip() for x in open("requirements.txt").readlines()]

setup(
    name="data_scraping",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements(),
)
