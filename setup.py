from setuptools import setup
version = '0.0.1'

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='pybud',
    version=version,
    install_requires=[
        'python-dateutil',
        'matplotlib'
    ],
    url='https://github.com/agzimmerman/pybud',
    license='MIT',
    author='Alexander G. Zimmerman',
    author_email='alex.g.zimmerman@gmail.com',
    description='A small package for personal accounting',
    keywords=['budget', 'personal finance', 'accounting'],
)
