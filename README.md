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

The dependencys ``colored``, ``click`` will be installed automatically.

## Command Line Usage

The files ``pysrec`` provides a command line interface.
Run the following command to see usage information:

```
$ ./pysrec --help
```

    Usage: pysrec [OPTIONS] COMMAND [ARGS]...
    
      Command line interface for pysrec. Use --help for details.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      binary  Generate a binary file from a Motorola S-Record file.
      cat     Print Motorola S-record file.
      check   Check a Motorola S-Record file.
      info    Show information about a Motorola S-Record file.

To get further information for each sub-command use for example:

```
$ ./pysrec cat --help
```

Using the following example file from
[Wikipedia SREC (file format)] (http://en.wikipedia.org/wiki/SREC_%28file_format%29)
we will take a deeper look at the usage.

    S00F000068656C6C6F202020202000003C
    S11F00007C0802A6900100049421FFF07C6C1B787C8C23783C6000003863000026
    S11F001C4BFFFFE5398000007D83637880010014382100107C0803A64E800020E9
    S111003848656C6C6F20776F726C642E0A0042
    S5030003F9
    S9030000FC

### cat sub-command

Lets say we only want do see the last two lines of our example file with their line numbers.

```
$ ./pysrec cat --start=-2 --lines example.srec
```

    [00000005] S5030003F9
    [00000006] S9030000FC

When using the `--color` option, the single S-Record fields for each record are colored differently to enhance the readability.

### info sub-command

Lets say we have just got our example S-Record file and we want to know a bit more about it.

```
$ ./pysrec info example.srec
```

    ================================================================================
    Analysing file: example.srec
    ================================================================================
    S-Records: 6
    MOT Type: S19
    Records:
        S0: 1
        S1: 3
        S5: 1
        S9: 1
    Header: hello!    
    Min. address: 0x0
    Max. address: 0x38
    ================================================================================

Now know its a S-record file of the type S19 and the min. and max. addresses. The info sub-command even printed the content of the S0 header record.

### check sub-command

For this example we will use a modified example file which contains some errors.

    S10F000068656C6C6F202020202000003C
    S11F00007C0802A6900100049421FFF07C6C1B787C8C23783C6000003863000027
    S11F001C4BFFFFE5398000007D83637880010014382100107C0803A64E800020E9
    S111003848656C6C6F20776F726C642E0A0086
    SF030003F9
    S9030000FC
    
Using the check sub-command we now can check the file for errors.

```
$ ./pysrec check example.srec
```

    ================================================================================
    Checking file: errors.srec
    ================================================================================
    Checking Record types...
    
    MOT Type: UNKNOWN
    
    Records:
    Invalid TYPE SF found 1 times
    
    Header:
    File has no S0 header record!
    ================================================================================
    Checking for invalid COUNT fields...
    
    Invalid COUNT: [00000004] SF030003F9F9
    ================================================================================
    Checking for invalid CRC fields...
    
    Invalid CRC: [00000001] S11F00007C0802A6900100049421FFF07C6C1B787C8C23783C6000003863000027
    Invalid CRC: [00000003] S111003848656C6C6F20776F726C642E0A0086
    Invalid CRC: [00000004] SF030003F9F9
    ================================================================================
