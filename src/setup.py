'''
Created on Oct 3, 2015

@author: fawix
'''

from distutils.core import setup

requirements = [
    "cairo",
]


setup(
    name='SniptIt',
    version='0.5dev',
    packages=['sniptit',],
    author='Fawix',
    description="Simple Screenshot Application for GNOME3",
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International',
    long_description=open('README.txt').read(),
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='gnome3 screenshot',
      
    data_files=[
        ('icon', [
            'snipit/snipit.ico',
        ])]
    
)
