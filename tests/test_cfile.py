import unittest

from cwrap import Prototype, CFILE, load


# Local copies so that the real ones don't get changed
class TestUtilPrototype(Prototype):
    lib = load("libert_util")
    def __init__(self, prototype, bind=False):
        super(TestUtilPrototype, self).__init__(TestUtilPrototype.lib, prototype, bind=bind)

fileno = TestUtilPrototype("int fileno(FILE)")


class CFILETest(unittest.TestCase):

    def test_cfile(self):
        return
        # TODO FIX THIS TO USE TMP
        # with TestAreaContext("cfile_tests") as test_area:

        #     with open("test", "w") as f:
        #         f.write("some content")

        #     with open("test", "r") as f:
        #         cfile = CFILE(f)

        #         self.assertEqual(fileno(cfile), f.fileno())

    def test_cfile_error(self):
        with self.assertRaises(TypeError):
            cfile = CFILE("some text")
