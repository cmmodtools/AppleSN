#!/usr/bin/env python
#
#  Copyright (C) 2013-2018 Michal Roszkowski
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import string

class AppleSN(object):
    """Apple Serial Number"""

    _Semester = {s: v for v,s in enumerate(
        (s for s in string.ascii_uppercase \
        if s not in {'A', 'E', 'I', 'O', 'U', 'B'}))}
    _Week = {w: v for v,w in enumerate(
        (w for w in string.digits + string.ascii_uppercase \
        if w not in {'A', 'E', 'I', 'O', 'U', 'B', '0', 'S', 'Z'}), start = 1)}

    def __init__(self, serial):
        self._serial = serial.upper()

        if not self._serial.isalnum():
            raise ValueError("Invalid serial number")

        if len(self) == 11:
            self._location = self._serial[:2]
            try:
                self._year = 2000 + int(self._serial[2])
                self._week = int(self._serial[3:5])
            except ValueError:
                raise ValueError("Invalid serial number")
            if self._week < 1 or self._week > 53:
                raise ValueError("Invalid serial number")

        elif len(self) == 12:
            self._location = self._serial[:3]
            try:
                self._year = 2010 + AppleSN._Semester[self._serial[3]] // 2
                self._week = 26 * (AppleSN._Semester[self._serial[3]] % 2) \
                             + AppleSN._Week[self._serial[4]]
            except KeyError:
                raise ValueError("Invalid serial number")

        else:
            raise ValueError("Invalid or unsupported serial number")

        self._id = self._serial[5:8]
        self._model = self._serial[8:]

    def __repr__(self):
        return self._serial

    def __len__(self):
        return len(self._serial)

    def __lt__(self, other):
        return self.week < other.week if self.year == other.year else \
               self.year < other.year

    @property
    def location(self):
        """Manufacturing Location"""
        return self._location

    @property
    def year(self):
        """Year of Manufacture"""
        return self._year

    @property
    def week(self):
        """Week of Manufacture"""
        return self._week

    @property
    def id(self):
        """Unique identifier"""
        return self._id

    @property
    def model(self):
        """Model Number"""
        return self._model

if __name__ == "__main__":
    import sys
    try:
        sn = AppleSN(sys.argv[1])
    except IndexError:
        print "Usage:", sys.argv[0], "SerialNumber"
        sys.exit(1)

    print "Serial Number:", sn
    print "Manufacturing Location:", sn.location
    print "Year of Manufacture:", sn.year
    print "Week of Manufacture:", sn.week
    print "Unique identifier:", sn.id
    print "Model Number:", sn.model
