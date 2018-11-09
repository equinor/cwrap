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
import six
import sys
from .prototype import Prototype
from .basecclass import BaseCClass


if six.PY2:
    import ctypes

    def copen(filename, mode='r'):
        """
        This is a compatibility layer for functions taking FILE* pointers, and
        should not be used unless absolutely needed.

        In Python 2 this function is simply an alias for open. In Python 3,
        however, it returns an instance of CWrapFile, a very light weight
        wrapper around a FILE* instance.
        """
        return open(filename, mode)

    class CFILE(BaseCClass):
        """
        Utility class to map a Python file handle <-> FILE* in C
        """
        TYPE_NAME = "FILE"

        _as_file = Prototype(ctypes.pythonapi, "void* PyFile_AsFile(py_object)")

        def __init__(self, py_file):
            """
            Takes a python file handle and looks up the underlying FILE *

            The purpose of the CFILE class is to be able to use python
            file handles when calling C functions which expect a FILE
            pointer. A CFILE instance should be created based on the
            Python file handle, and that should be passed to the function
            expecting a FILE pointer.

            The implementation is based on the ctypes object
            pythonapi which is ctypes wrapping of the CPython api.

              C-function:
                 void fprintf_hello(FILE * stream , const char * msg);

              Python wrapper:
                 lib = clib.load( "lib.so" )
                 fprintf_hello = Prototype(lib, "void fprintf_hello( FILE , char* )")

              Python use:
                 py_fileH = open("file.txt" , "w")
                 fprintf_hello( CFILE( py_fileH ) , "Message ...")
                 py_fileH.close()

            If the supplied argument is not of type py_file the function
            will raise a TypeException.

            Examples: ecl.ecl.ecl_kw.EclKW.fprintf_grdecl()
            """
            c_ptr = self._as_file(py_file)
            try:
                super(CFILE, self).__init__(c_ptr)
            except ValueError:
                raise TypeError("Sorry - the supplied argument is not a valid "
                                " Python file handle!")

            self.py_file = py_file

        def __del__(self):
            pass


if six.PY3:
    from .clib import load as cwrapload

    class LibcPrototype(Prototype):
        # Load the c standard library (on Linux passsing None does the trick)
        lib = cwrapload('msvcrt' if os.name == 'nt' else None)

        def __init__(self, prototype, bind=False, allow_attribute_error=False):
            super(LibcPrototype, self).__init__(
                LibcPrototype.lib,
                prototype,
                bind=bind,
                allow_attribute_error=allow_attribute_error)

    def copen(filename, mode='r'):
        """
        This is a compatibility layer for functions taking FILE* pointers, and
        should not be used unless absolutely needed.

        In Python 2 this function is simply an alias for open. In Python 3,
        however, it returns an instance of CWrapFile, a very lightweight
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
                super(CWrapFile, self).__init__(c_ptr)
            except ValueError:
                self._closed = True
                raise IOError('Could not open file "{}" in mode {}'
                              .format(fname, mode))

        def close(self):
            if not self._closed:
                self._fflush()
                cs = self._fclose()
                if (cs != 0):
                    raise IOError("Failed to close file")
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
            raise TypeError("This function requires the use of CWrapFile, "
                            "not {} when running Python 3. See "
                            "help(cwrap.open) for more info"
                            .format(type(f).__name__))
        return f
