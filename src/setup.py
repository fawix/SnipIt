'''
Created on Oct 3, 2015

@author: fawix
'''

#from distutils.core import setup
from setuptools import setup

requirements = [
    "cairo",
]


setup(
    name='SniptIt',
    version='0.7dev',
    packages=['snipit',],
    author='Fawix',
    description="Simple Screenshot Application for GNOME3",
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International',
    long_description=open('README.txt').read(),
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='gnome3 screenshot',
    
    entry_points={
        'gui_scripts': [
            'snipit=snipit.snipit:main'
        ], 
        'console_scripts': [
            'snipit=snipit.snipit:main',
        ]
    },
      
    data_files=[
        ('icon', [
            'snipit/snipit.ico',
        ])]
    
)
