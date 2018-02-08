import os
import shutil
import tempfile

import unittest

from cwrap import Prototype, CFILE, load, open as copen

# Local copies so that the real ones don't get changed
class TestUtilPrototype(Prototype):
    lib = load(None)
    def __init__(self, prototype, bind=False):
        super(TestUtilPrototype, self).__init__(TestUtilPrototype.lib, prototype, bind=bind)

fileno = TestUtilPrototype("int fileno(FILE)")


class CFILETest(unittest.TestCase):

    def test_cfile(self):
        cwd = os.getcwd()
        d = tempfile.mkdtemp( )
        os.chdir( d )

        with open("test", "w") as f:
            f.write("some content")

        with copen("test", "r") as f:
            cfile = CFILE(f)
            self.assertTrue(fileno(cfile))

        os.chdir(cwd)
        shutil.rmtree( d )



    def test_cfile_error(self):
        with self.assertRaises(TypeError):
            cfile = CFILE("some text")
