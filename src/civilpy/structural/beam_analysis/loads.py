"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Dependency imports
from dataclasses import dataclass
import numpy as np



@dataclass()
class PointLoad:

    nodeID = None

    def __init__(self, P, x, nodeID=None, label=''):
        self.P = P
        self.x = x
        self.nodeID = nodeID
        self.label = label
        self.loadPattern = None

    def _setID(self, newID):
        self.nodeID = newID

    def getPosition(self):
        return self.x


@dataclass()
class EleLoadDist:

    def __init__(self, x1: float, x2: float, distLoad: list, label: str = ''):
        self.x1 = x1
        self.x2 = x2
        self.P = distLoad
        self.label = label


@dataclass()
class EleLoadLinear:

    def __init__(self, x1: float, x2: float, linLoad: list, label: str = ''):

        self.x1 = x1
        self.x2 = x2
        self.P = linLoad
        self.label = label
        self.Lnet = x2 - x1

    def checkInRange(self, s):


        if s < self.x1:
            raise Exception(r'First point range, must be greater than {x1}')

        if self.x2 < s:
            raise Exception(r'Second point range, must be less than {self.x2}')

    def getLoadComponents(self, s1, s2, q):

        self.checkInRange(s1)
        self.checkInRange(s2)
        s1 = (s1 - self.x1) / self.Lnet
        s2 = (s2 - self.x1) / self.Lnet

        m = q[1] - q[0]

        y1 = s1 * m + q[0]
        y2 = s2 * m + q[0]

        return y1, y2


@dataclass
class PointLoadOptions:
    # GlobalParameters
    lw: float
    c: float  # colour
    arrowWidth: float


@dataclass
class DistLoadOptions:
    # GlobalParameters
    baseWidth: float
    c: float  # colour
    arrowWidth: float

    spacing: float
    barWidth: float


@dataclass
class LinLoadOptions:
    # GlobalParameters
    baseWidth: float
    c: float  # colour
    arrowWidth: float

    spacing: float
    barWidth: float
    minLengthCutoff: float


@dataclass
class MomentPointLoadOptions:
    # GlobalParameters
    lw: float
    c: float  # colour
    arrowWidth: float

    # Circle parameters
    r: float
    rotationAngle: float


class EleLoadBox:
    def __init__(self, x: tuple[float], y: tuple[float], fint: tuple[float] = None,
                 intDatum: float = None):
        self.x = x
        self.y = y

        self.x.sort()
        self.y.sort()

        if fint == None:
            fint = [1, 1]

        self.fint = fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]

        # If the internal datum is manually set
        if intDatum:
            self.intDatum = intDatum
            self.datum = self._interpolate(intDatum)

            sign1 = np.sign(self.fout[0])
            sign2 = np.sign(self.fout[1])
            if sign1 == sign2 >= 0:
                self.changedDirection = False
            else:
                self.changedDirection = True

        # If there is no internal datum, this is the typical case.
        else:
            self._initInternalDatum()

    def setDatum(self, datum):
        dy = datum - self.datum
        self.y = [self.y[0] + dy, self.y[1] + dy]
        self.datum = datum

        fint = self.fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]

    def shiftDatum(self, dy):
        self.y = [self.y[0] + dy, self.y[1] + dy]
        self.datum = self.datum + dy

        fint = self.fint
        self.fout = [self._interpolate(fint[0]), self._interpolate(fint[1])]

    def getInternalDatum(self):
        return self.datum

    def _interpolate(self, fint):
        return (self.y[1] - self.y[0]) * fint + self.y[0]

    def _initInternalDatum(self):

        sign1 = np.sign(self.fout[0])
        sign2 = np.sign(self.fout[1])

        self.datum = 0
        if sign1 >= 0 and sign2 >= 0:
            self.changedDirection = False
            self.intDatum = 0

        elif sign1 <= 0 and sign2 <= 0:
            self.changedDirection = False
            self.intDatum = 1
        else:
            self.changedDirection = True
            dy = self.y[0] - self.y[1]
            self.intDatum = self.y[0] / dy

    @property
    def isConstant(self):
        return self.fint[0] == self.fint[1]
