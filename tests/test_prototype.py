import os

import pytest

from cwrap import BaseCClass, Prototype, load


class LibCPrototype(Prototype):
    lib = load("msvcrt" if os.name == "nt" else None)

    def __init__(self, prototype, bind):
        super().__init__(LibCPrototype.lib, prototype, bind=bind)


class BadInitialization(BaseCClass):
    TYPE_NAME = "bad_initialization"
    _abs = LibCPrototype("int abs(int)", bind=True)

    def __init__(self):
        self._abs(0)  # called before initialization, should raise

    def free(self):
        pass


def test_that_unitialized_is_raised():
    with pytest.raises(ValueError, match="uninitialized"):
        _ = BadInitialization()
