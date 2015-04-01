# Python SREC Tools

**pysrec** is a Python 3 module for handling Motorola S-Record files.
It also delivers a command line tool to perform basic interaction with S-Record files.

## Note

On machines where Python 3 is not the default Python runtime, you should use
``pip3`` instead of ``pip``.

## Prerequisites

```
$ sudo apt-get install python3 python3-pip
```

## Installation

Install the module by running:

```
$ unzip pysrec-*.zip
$ pip install pysrec
```

The dependencys ``matplotlib``, ``colored``, ``click``, ``numpy`` will be installed automatically.

## Command Line Usage

The files ``pysrec`` provides a command line interface.
Run the following command to see usage information:

```
$ ./pysrec --help
```
