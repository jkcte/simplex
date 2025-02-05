from setuptools import setup, find_packages

setup(
    name='simplex',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Milk Puncher',
    author_email='2022037221@feu.edu.ph',
    description='A package to solve linear programming problems using the Simplex method',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jkcte/simplex',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)