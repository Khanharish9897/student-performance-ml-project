from setuptools import find_packages,setup
from typing import List
HYPHEN_E_DOT = "-e ."
def get_requirements(filepath:str)->List[str]:
    '''
    this fxn return list of requirements
    :param filepath:
    :return:
    '''

    requirements = []
    with open(filepath, "r") as file:
        requirements = file.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements




setup(
    name='student performance project',
    version='0.0.1',
    packages=find_packages(),
    author='Harish khan',
    author_email='khanharish9897@gmail.com',
    install_requires=get_requirements("r.txt")
)