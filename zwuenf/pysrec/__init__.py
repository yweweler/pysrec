"""
This API can be used to interact with and modify Motorola S-Record files.

.. moduleauthor:: Yves-Noel Weweler <y.weweler@gmail.com>
"""

__author__ = 'Yves-Noel Weweler <y.weweler@gmail.com>'
__status__ = 'Development'
__version__ = '0.0.1'
__all__ = ('SRECError', 'SRecordParsingError', 'NotSRecFileError')


class SRECError(Exception):
    """
    General error of this module. All other exceptions are derived from
    this class.
    """
    pass


class SRecordParsingError(SRECError):
    """
    Parsing a single S-Record failed.
    """
    pass


class NotSRecFileError(SRECError):
    """
    Given file is not a Motorola S-Record file.
    """
    pass