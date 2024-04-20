from setuptools import find_packages , setup
from typing import List

def get_requirments(file_path:str) -> List[str]:
    '''
    this function will return listof requirmnets
    '''
    HYPEN_E_DOT = '-e .'
    requriments = []
    with open(file_path) as file_object:
        requriments = file_object.readlines()
        requriments = [i.replace('\n' , '') for i in requriments]

        if HYPEN_E_DOT in requriments:
            requriments.remove(HYPEN_E_DOT)
    return requriments


setup(
name='mlproject' ,
version=0.01,
author='Krishna',
author_email='saik36048@gmail.com',
packages=find_packages() ,
install_requires =get_requirments('requriments.txt')

)