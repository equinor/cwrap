#  Copyright (C) 2016  Statoil ASA, Norway.
#
#  This file is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.

import os

from .basecclass import BaseCClass
from .clib import load as cwrapload
from .prototype import Prototype


class LibcPrototype(Prototype):
    # Load the c standard library (on Linux passsing None does the trick)
    lib = cwrapload("msvcrt" if os.name == "nt" else None)

    def __init__(self, prototype, bind=False, allow_attribute_error=False):
        super().__init__(
            LibcPrototype.lib,
            prototype,
            bind=bind,
            allow_attribute_error=allow_attribute_error,
        )


def copen(filename, mode="r"):
    """
    This is a compatibility layer for functions taking FILE* pointers, and
    should not be used unless absolutely needed.

    It returns an instance of CWrapFile, a very lightweight
    wrapper around a FILE* instance.
    """
    return CWrapFile(filename, mode)


class CWrapFile(BaseCClass):
    """
    This is a compatibility layer for functions taking FILE* pointers, and
    should not be used unless absolutely needed.

    CWrapFile is a very lightweight wrapper around FILE* instances. It is
    meant be used inplace of python file objects that are to be passed to
    foreign function calls under python 3.

    Example:
        with cwrap.open('filename', 'mode') as f:
            foreign_function_call(f)
    """

    TYPE_NAME = "FILE"

    _fopen = LibcPrototype("void* fopen (char*, char*)")
    _fclose = LibcPrototype("int fclose (FILE)", bind=True)
    _fflush = LibcPrototype("int fflush (FILE)", bind=True)

    def __init__(self, fname, mode):
        c_ptr = self._fopen(fname, mode)
        self._mode = mode
        self._fname = fname
        self._closed = False

        try:
            super().__init__(c_ptr)
        except ValueError as err:
            self._closed = True
            raise OSError(f'Could not open file "{fname}" in mode {mode}') from err

    def close(self):
        if not self._closed:
            self._fflush()
            cs = self._fclose()
            if cs != 0:
                raise OSError("Failed to close file")
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type is None

    def free(self):
        self.close()

    def __del__(self):
        self.close()


def CFILE(f):
    if not isinstance(f, CWrapFile):
        raise TypeError(
            "This function requires the use of CWrapFile, "
            f"not {type(f).__name__} when running Python 3. See "
            "help(cwrap.open) for more info"
        )
    return f
