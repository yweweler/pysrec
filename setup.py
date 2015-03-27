import os

from setuptools import setup, find_packages


def get_version():
    path = os.path.join(os.path.dirname(__file__), 'zwuenf/pysrec/__init__.py')
    with open(path) as file:
        for line in file:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
# Import long description
long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='zwuenf.pysrec',
    version=get_version(),
    packages=find_packages(),
    namespace_packages=['zwuenf'],
    install_requires=[
        'click>=3.3',
        'matplotlib>=1.4.3',
        'colored>=1.1.5',
        'numpy>=1.9.2'
    ],
    include_package_data=True,


    # PyPI metadata
    author='Yves-Noel Weweler',
    author_email='y.weweler@gmail.com',
    description=('This API can be used to interact with and modify Motorola S-Record files.'),
    long_description=long_description,
    license='MIT License',
    keywords='zwuenf pysrec srec api',
    url='http://zwuenf.de/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
