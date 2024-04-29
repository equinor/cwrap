import os
import shutil
import tempfile
import unittest

from cwrap import CFILE, Prototype, load
from cwrap import open as copen


# Local copies so that the real ones don't get changed
class ForTestUtilPrototype(Prototype):
    lib = load("msvcrt" if os.name == "nt" else None)

    def __init__(self, prototype, bind=False):
        super().__init__(ForTestUtilPrototype.lib, prototype, bind=bind)


fileno = ForTestUtilPrototype("int fileno(FILE)")


class CFILETest(unittest.TestCase):
    def test_cfile(self):
        cwd = os.getcwd()
        d = tempfile.mkdtemp()
        os.chdir(d)

        with open("test", "w") as f:
            f.write("some content")

        with copen("test", "r") as f:
            cfile = CFILE(f)
            if os.name != "nt":
                self.assertTrue(fileno(cfile))

        os.chdir(cwd)
        shutil.rmtree(d)

    def test_cfile_error(self):
        with self.assertRaises(TypeError):
            CFILE("some text")
