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
from dataclasses import dataclass
from matplotlib.patches import Rectangle, Polygon, Circle
import numpy as np

from .diagram import AbstractDiagramElement

@dataclass
class supportDiagramOptions:
    # GlobalParameters
    lw: float
    scale: float
    supScale: float

    #
    r: float

    # Parameters for the triangle
    hTriSup: float
    wTriSup: float

    # Parameters for the rectangle below the support
    hFixedRect: float
    marginFixedSup: float
    hatch: str
    wRect: float

    # Roller
    lineOffset_roller: float
    hRollerGap: float
    y0: float

class DiagramElePinSupport(AbstractDiagramElement):
    def __init__(self, xy0, diagramOptions: supportDiagramOptions):
        self.xy0 = xy0
        self.options = diagramOptions

    def _getPinSupportCords(self, xy0, scale):

        wTriSup = self.options.wTriSup
        hTriSup = self.options.hTriSup
        wRect = self.options.wRect
        hFixedRect = self.options.hFixedRect

        xyTri1 = [xy0[0] - wTriSup / 2, xy0[1] - hTriSup]
        xyTri2 = [xy0[0] + wTriSup / 2, xy0[1] - hTriSup]
        xyTri = [xyTri1, xyTri2, xy0]

        xy0Rect = [xy0[0] - wRect / 2, xy0[1] - hTriSup - hFixedRect]

        xyLine = [[xy0[0] - wRect / 2, xy0[0] + wRect / 2],
                  [xy0[1] - hTriSup - hFixedRect, xy0[1] - hTriSup - hFixedRect]]

        return xyTri, xy0Rect, xyLine

    def _plotPinGeom(self, ax, xy0, xyTri, xy0Rect, xyLine):

        #
        lw = self.options.lw
        hatch = self.options.hatch
        wRect = self.options.wRect
        r = self.options.r
        hFixedRect = self.options.hFixedRect

        ax.add_patch(Polygon(xyTri, fill=False, lw=lw))
        ax.add_patch(Rectangle(xy0Rect, wRect, hFixedRect, ec='black', fc='white', hatch=hatch, lw=lw))
        ax.plot(xyLine[0], xyLine[1], c='white', lw=lw)
        ax.add_patch(Circle(xy0, r, facecolor='white', ec='black', fill=True, zorder=1, lw=lw))

    def plot(self, ax):

        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(self.xy0, scale)
        self._plotPinGeom(ax, self.xy0, xyTri, xy0Rect, xyLine)


class DiagramEleRollerSupport(DiagramElePinSupport):

    def __init__(self, xy0, diagramOptions: supportDiagramOptions):
        self.xy0 = xy0
        self.options = diagramOptions

    def _getRollerSupportCords(self, xy0, scale):


        lineOffset = self.options.lineOffset_roller
        hTriSup = self.options.hTriSup
        hRollerGap = self.options.hRollerGap
        wRect = self.options.wRect

        # The gap starts a the botom-left surface of the roller
        xy0gap = [xy0[0] - wRect / 2, xy0[1] - hTriSup + lineOffset]

        # The line starts at the top of the gap
        xyRollerLine = [[xy0[0] - wRect / 2, xy0[0] + wRect / 2],
                        [xy0[1] - hTriSup + hRollerGap + lineOffset,
                         xy0[1] - hTriSup + hRollerGap + lineOffset]]

        return xy0gap, xyRollerLine

    def _plotRollerGeom(self, ax, xy0gap, xyRollerLine):
        lw = self.options.lw
        hRollerGap = self.options.hRollerGap
        wRect = self.options.wRect

        ax.add_patch(Rectangle(xy0gap, wRect, hRollerGap, color='white', lw=lw))
        ax.plot(xyRollerLine[0], xyRollerLine[1], color='black', lw=lw)

    def plotRoller(self, ax):

        xy0 = self.xy0
        scale = self.options.scale
        xyTri, xy0Rect, xyLine = self._getPinSupportCords(xy0, scale)
        self._plotPinGeom(ax, xy0, xyTri, xy0Rect, xyLine)
        xy0gap, xyRollerLine = self._getRollerSupportCords(xy0, scale)
        self._plotRollerGeom(ax, xy0gap, xyRollerLine)

    def plot(self, ax):


        self.plotRoller(ax)


class DiagramEleFreeSupport:
    def __init__(self, xy, diagramOptions: supportDiagramOptions):
        pass

    def plot(self, ax):
        pass


class DiagramEleFixedSupport(AbstractDiagramElement):

    def __init__(self, xy0, diagramOptions: supportDiagramOptions,
                 isLeft=True):
        self.xy0 = xy0
        self.options = diagramOptions
        self.isLeft = isLeft

    def _getFixedSupportCords(self, xy0, isLeft):


        wRect = self.options.wRect
        hFixedRect = self.options.hFixedRect

        if isLeft:
            xy0Rect = [xy0[0] - hFixedRect, xy0[1] - wRect / 2]

            xyLine = [[xy0[0], xy0[0] - hFixedRect, xy0[0] - hFixedRect, xy0[0]],
                      [xy0[1] + wRect / 2, xy0[1] + wRect / 2,
                       xy0[1] - wRect / 2, xy0[1] - wRect / 2]]
        else:
            xy0Rect = [xy0[0], xy0[1] - wRect / 2]
            xyLine = [[xy0[0], xy0[0] + hFixedRect, xy0[0] + hFixedRect, xy0[0]],
                      [xy0[1] + wRect / 2, xy0[1] + wRect / 2,
                       xy0[1] - wRect / 2, xy0[1] - wRect / 2]]

        return xy0Rect, xyLine

    def plot(self, ax):


        lw = self.options.lw
        hFixedRect = self.options.hFixedRect
        hatch = self.options.hatch
        wRect = self.options.wRect
        xy0 = self.xy0

        isLeft = self.isLeft
        xy0Rect, xyLine = self._getFixedSupportCords(xy0, isLeft)
        ax.add_patch(Rectangle(xy0Rect, hFixedRect, wRect, ec='black',
                               fc='white', hatch=hatch, lw=lw))
        ax.plot(xyLine[0], xyLine[1], c='white', lw=lw)


class Fixity:
    def __init__(self, name: str, fixityValues: list[int]):

        self.name = name
        self.fixityValues = fixityValues

    def __repr__(self):
        return f'<Fixity type {self.name} with {self.fixityValues}.>'


class FixityTypes2D:
    releaseNames = ['free', 'roller', 'pinned', 'fixed']
    releaseTypes = [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 1, 1]]
    free = Fixity(releaseNames[0], releaseTypes[0])
    roller = Fixity(releaseNames[1], releaseTypes[1])
    pinned = Fixity(releaseNames[2], releaseTypes[2])
    fixed = Fixity(releaseNames[3], releaseTypes[3])
    types2D = {releaseNames[0]: free, releaseNames[1]: roller,
               releaseNames[2]: pinned, releaseNames[3]: fixed}

    @classmethod
    def getFree(cls):
        return cls.free

    @classmethod
    def getRoller(cls):
        return cls.roller

    @classmethod
    def getPinned(cls):
        return cls.pinned

    @classmethod
    def getFixed(cls):
        return cls.fixed

NAMED_RELEASES_2D = set(FixityTypes2D.releaseNames)

def _getFixitystr(fixityInput):
    if fixityInput in FixityTypes2D.types2D.keys():
        return FixityTypes2D.types2D[fixityInput]
    else:
        raise Exception('fixity of type, {fixityInput} not supported, use one of', FixityTypes2D.keys())


def _getFixitylist(fixityInput):
    if list(fixityInput) == [0, 0, 0]:
        return FixityTypes2D.free
    elif list(fixityInput) == [0, 1, 0]:
        return FixityTypes2D.roller
    elif list(fixityInput) == [1, 1, 0]:
        return FixityTypes2D.pinned
    elif list(fixityInput) == [1, 1, 1]:
        return FixityTypes2D.fixed
    else:
        return Fixity('other', fixityInput)


def _convertFixityInput2D(fixityInput) -> Fixity:
    if isinstance(fixityInput, Fixity):
        return fixityInput

    if isinstance(fixityInput, list) or isinstance(fixityInput, np.ndarray):
        return _getFixitylist(fixityInput)

    if isinstance(fixityInput, str):
        return _getFixitystr(fixityInput)

    else:
        raise Exception('Given input not supported')