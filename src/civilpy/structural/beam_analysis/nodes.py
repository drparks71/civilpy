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
from abc import ABC, abstractmethod
from typing import Union
import numpy as np

from .supports import Fixity, _convertFixityInput2D


class NodeArchetype(ABC):

    @abstractmethod
    def getFixityType(self):

        pass

    @abstractmethod
    def getPosition(self):


        pass

    @abstractmethod
    def getLabel(self):

        pass



class Node(NodeArchetype):

    _dimension = '2D'  # the number for forces that can be applied
    _Nforce = 3  # the number for forces that can be applied

    def __init__(self, x: float, fixity: Union[list, str, Fixity], label: str = ''):

        self.x = x
        self.fixity = _convertFixityInput2D(fixity)
        self.ID = None
        self.label = label
        self.labelIsPlotted = False

        self.pointLoadIDs = []

        self.disp = None
        self.rFrc = None
        self.Fint = None

        self.averageShear = False

        self._setHasReaction()

    def _setHasReaction(self):
        self.hasReaction = False
        fixities = np.array(self.fixity.fixityValues)
        if np.any(fixities == np.array([1] * self._Nforce, int)):
            self.hasReaction = True

    def _setID(self, newID):

        self.ID = newID

    def __repr__(self):
        return f'{self._dimension} Node object at {self.x}'

    def getLabel(self):
        return self.label

    def getPosition(self):
        return self.x

    def _checkIfResultsAveraged(self):
        if self.hasReaction == False and len(self.pointLoadIDs) == 0:
            return True
        return False

    def getInternalForces(self, ind):


        return self.Fint[[ind, ind + self._Nforce]]


class Node2D(Node):

    _dimension = '2D'  # the number for forces that can be applied
    _Nforce = 3  # the number for forces that can be applied

    def __init__(self, x: float, fixity: Union[list, str, Fixity], label: str = ''):
        super().__init__(x, fixity, label)

    def getFixityType(self):


        return self.fixity.name


class Node3D(Node):

    _dimension = '3D'  # the number for forces that can be applied
    _Nforce = 6  # the number for forces that can be applied

    def __init__(self, x: float, fixity: Union[list, str, Fixity], label: str = ''):
        super().__init__(x, fixity, label)

    def getFixityType(self):

        raise Exception('Plotting for 3D beams not yet supported')