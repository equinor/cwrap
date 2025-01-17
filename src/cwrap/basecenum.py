#  Copyright (C) 2016 Statoil ASA, Norway.
#
#  This file is part of cwrap.
#
#  cwrap is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  cwrap is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.

import ctypes

from .metacwrap import MetaCWrap


class BaseCEnum(metaclass=MetaCWrap):
    enum_namespace = {}

    def __init__(self, *args, **kwargs):
        if not self in self.enum_namespace[self.__class__]:
            raise NotImplementedError("Can not be instantiated directly!")

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            enum = cls.__resolveEnum(args[0])

            if enum is None:
                raise ValueError(f"Unknown enum value: {args[0]}")

            return enum
        else:
            obj = super().__new__(cls, *args)
            obj.name = None
            obj.value = None
            return obj

    @classmethod
    def from_param(cls, c_class_object):
        if not isinstance(c_class_object, BaseCEnum):
            raise ValueError("c_class_object must be an BaseCEnum instance!")
        return c_class_object.value

    @classmethod
    def from_string(cls, name):
        for enum in cls.enum_namespace[cls]:
            if enum.name == name:
                return enum

        raise ValueError(f"No such enum: {name}")

    @classmethod
    def addEnum(cls, name, value):
        name = str(name)
        if not isinstance(value, int):
            raise ValueError("Value must be an integer!")

        enum = cls.__new__(cls)
        enum.name = name
        enum.value = value

        setattr(cls, name, enum)

        if cls not in cls.enum_namespace:
            cls.enum_namespace[cls] = []

        cls.enum_namespace[cls].append(enum)

    @classmethod
    def enums(cls):
        return list(cls.enum_namespace[cls])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

        if isinstance(other, int):
            return self.value == other

        return False

    def is_initialized(self):
        return True

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.name

    def __repr__(self):
        cn = self.__class__.__name__
        na = self.name
        va = self.value
        return f'{cn}(name = "{na}", value = {va})'

    def __add__(self, other):
        self.__assertOtherIsSameType(other)
        value = self.value + other.value
        return self.__resolveOrCreateEnum(value)

    def __or__(self, other):
        self.__assertOtherIsSameType(other)
        value = self.value | other.value
        return self.__resolveOrCreateEnum(value)

    def __xor__(self, other):
        self.__assertOtherIsSameType(other)
        value = self.value ^ other.value
        return self.__resolveOrCreateEnum(value)

    def __and__(self, other):
        self.__assertOtherIsSameType(other)
        value = self.value & other.value
        return self.__resolveOrCreateEnum(value)

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __contains__(self, item):
        return self & item == item

    @classmethod
    def __createEnum(cls, value):
        enum = cls.__new__(cls)
        enum.name = f"Unnamed '{cls.__name__}' enum with value: {value}"
        enum.value = value
        return enum

    @classmethod
    def __resolveOrCreateEnum(cls, value):
        enum = cls.__resolveEnum(value)

        if enum is not None:
            return enum

        return cls.__createEnum(value)

    @classmethod
    def __resolveEnum(cls, value):
        for enum in cls.enum_namespace[cls]:
            if enum.value == value:
                return enum
        return None

    def __assertOtherIsSameType(self, other):
        assert isinstance(other, self.__class__), (
            f"Can only operate on enums of same type: {self.__class__.__name__} != {other.__class__.__name__}"
        )

    @classmethod
    def populateEnum(cls, library, enum_provider_function):
        try:
            func = getattr(library, enum_provider_function)
        except AttributeError as err:
            raise ValueError(
                f"Could not find enum description function: {enum_provider_function} - can not load enum: {cls.__name__}."
            ) from err

        func.restype = ctypes.c_char_p
        func.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]

        index = 0
        while True:
            value = ctypes.c_int()
            name = func(index, ctypes.byref(value))

            if name:
                cls.addEnum(name, value.value)
                index += 1
            else:
                break
