from setuptools import find_packages ,setup
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements = []
    with open(file_path,'r') as f:
        requirements = f.readlines()
        requirements = [req.replace('\n','') for req in requirements]
        # print(requirements)
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements
# setupn file use case 
# This project is a package. Here is its name, version, dependencies, and how to install it. 

# -e . Installs the package in editable mode. Changes to your code are available immediately.
setup(
    name='ml_project',
    version='0.0.1',
    author='ArmanJamwal',
    author_email='armanjamwal129@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)