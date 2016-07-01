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

from cwrap import MetaCWrap



class BaseCEnum(object):
    __metaclass__ = MetaCWrap
    _enum_namespace = {}

    def __init__(self, *args, **kwargs):
        if not self in self._enum_namespace[self.__class__]:
            raise NotImplementedError("Can not be instantiated directly!")

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            enum = cls._resolveEnum(args[0])

            if enum is None:
                raise ValueError("Unknown enum value: %i" % args[0])

            return enum
        else:
            obj = super(BaseCEnum, cls).__new__(cls, *args)
            obj.name = None
            obj.value = None
            return obj

    @classmethod
    def from_param(cls, c_class_object):
        if not isinstance(c_class_object, BaseCEnum):
            raise ValueError("c_class_object must be an BaseCEnum instance!")
        return c_class_object.value

    @classmethod
    def addEnum(cls, name, value):
        if not isinstance(value, int):
            raise ValueError("Value must be an integer!")

        enum = cls.__new__(cls)
        enum.name = name
        enum.value = value

        setattr(cls, name, enum)

        if not cls._enum_namespace.has_key(cls):
            cls._enum_namespace[cls] = []

        cls._enum_namespace[cls].append(enum)
        cls._enum_namespace[cls] = sorted(cls._enum_namespace[cls], key=BaseCEnum.__int__)

    @classmethod
    def enums(cls):
        return list(cls._enum_namespace[cls])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value

        if isinstance(other, int):
            return self.value == other

        return False

    def __str__(self):
        return self.name

    def __add__(self, other):
        self._assertOtherIsSameType(other)
        value = self.value + other.value
        return self._resolveOrCreateEnum(value)

    def __or__(self, other):
        self._assertOtherIsSameType(other)
        value = self.value | other.value
        return self._resolveOrCreateEnum(value)


    def __xor__(self, other):
        self._assertOtherIsSameType(other)
        value = self.value ^ other.value
        return self._resolveOrCreateEnum(value)

    def __and__(self, other):
        self._assertOtherIsSameType(other)
        value = self.value & other.value
        return self._resolveOrCreateEnum(value)

    def __int__(self):
        return self.value

    def __contains__(self, item):
        return self & item == item

    def __repr__(self):
        return str(self)

    @classmethod
    def _createEnum(cls, value):
        enum = cls.__new__(cls)
        enum.name = "Unnamed '%s' enum with value: %i" % (str(cls.__name__), value)
        enum.value = value
        return enum

    @classmethod
    def _resolveOrCreateEnum(cls, value):
        enum = cls._resolveEnum(value)

        if enum is not None:
            return enum

        return cls._createEnum(value)

    @classmethod
    def _resolveEnum(cls, value):
        for enum in cls._enum_namespace[cls]:
            if enum.value == value:
                return enum
        return None

    def _assertOtherIsSameType(self, other):
        assert isinstance(other, self.__class__), "Can only operate on enums of same type: %s =! %s" % (
            self.__class__.__name__, other.__class__.__name__)

