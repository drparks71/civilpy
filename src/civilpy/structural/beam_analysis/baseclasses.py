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
import numpy as np
from typing import Union


from .supports import Fixity, FixityTypes2D, _convertFixityInput2D, supportDiagramOptions
from .loads import (PointLoad, EleLoadDist, EleLoadLinear, PointLoadOptions, MomentPointLoadOptions, DistLoadOptions,
                    LinLoadOptions)
from .configure import LabelOptions
from .nodes import Node, Node2D, Node3D


class Section:
    E: float = None
    G: float = None
    A: float = None
    Iz: float = None
    Iy: float = None
    J: float = None


@dataclass
class SectionRectangle(Section):

    E: float = 200 * 10 ** 9
    d: float = 1
    w: float = 1
    G: float = None
    units: str = 'm'

    def __post_init__(self):
        if not self.G:
            self.G = self.E / 16

        self.A = self.d * self.w
        self.Iz = self.d ** 3 * self.w / 12
        self.Iy = self.w ** 3 * self.d / 12

        a = min(self.d, self.w)
        b = max(self.d, self.w)
        self.J = a ** 3 * b * (1 / 3 - 0.21 * a / b * (1 - (a ** 4 / (12 * b ** 4))))


@dataclass
class SectionBasic(Section):

    E: float = 1
    G: float = 1
    A: float = 1
    Iz: float = 1
    Iy: float = 1
    J: float = 1


@dataclass
class BeamOptions:
    lw:float
    c:float


class Beam:
    _dimension = ''
    _ndf = None
    _NodeTypes = {'2D': Node2D, '3D': Node3D}
    _activeNodeType = None

    def _initDimensionVariables(self, dimension):
        self._dimension = dimension
        if dimension == '2D':
            self._ndf = 3
        elif dimension == '3D':
            self._ndf = 6
        self._activeNodeType = self._NodeTypes[self._dimension]

    def getDOF(self):

        return self._ndf

    def _initArrays(self):
        self.nodeLabels = {}
        self.nodes: list[Node] = []
        self.Nnodes = 0
        self.pointLoads = []
        self.distLoads = []
        self.nodeCoords = set()

    def getLength(self):

        return self.nodes[-1].x - self.nodes[0].x

    def getxLims(self):


        return self.nodes[0].x, self.nodes[-1].x

    def _sortNodes(self):

        xcoords = np.zeros(self.Nnodes)
        labels = [None] * self.Nnodes
        for ii, node in enumerate(self.nodes):
            xcoords[ii] = node.x
            labels[ii] = node.label

        # subtract 1 because the indexes are one less.
        oldInd = np.array(self.getNodeIDs())

        # Sort the nodes.
        sortedInd = np.argsort(xcoords)
        sortedNodes = np.array(self.nodes)[sortedInd]
        self.nodes = list(sortedNodes)

        self._resetNodeID()
        self._remapLabels(sortedInd)
        self._remapPointLoads(oldInd, sortedInd)

    def getNodeIDs(self):


        IDs = [None] * self.Nnodes
        for ii, node in enumerate(self.nodes):
            IDs[ii] = node.ID

        return IDs

    def _resetNodeID(self):

        for ii, node in enumerate(self.nodes):
            node._setID(int(ii + 1))

    def _remapPointLoads(self, oldIDs, sortedInd):

        sortedIDs = np.array(oldIDs)[sortedInd]
        for pointLoad in self.pointLoads:
            newInd = np.where(sortedIDs == pointLoad.nodeID)[0][0] + 1
            pointLoad.nodeID = newInd

    def _remapLabels(self, sortedInd):

        oldLabels = self.nodeLabels
        newLabel = {}

        for label in oldLabels:
            newLabel[label] = sortedInd[oldLabels[label]]
        self.nodeLabels = newLabel

    def _addedNodeMessage(self, x):
        print(f'New node added at: {x}')

    def addNode(self, x: float, fixity: Union[list, str, Fixity] = None,
                label: str = '', sort: bool = True):

        if fixity is None:
            fixity = Fixity('free', np.zeros(self._ndf, int))
        newNode = self._activeNodeType(x, fixity, label)
        if x in self.nodeCoords:

            index = self._findNode(x)
            nodeID = self.nodes[index].ID
            newNode._setID(nodeID)

            if label is not None:
                newNode.label = label

            self.nodes[index] = newNode
            return 0
        else:
            self._addNewNode(newNode, sort)
            return 1
        return -1

    def addLabel(self, x: float, label: str, sort: bool = True):


        fixity = Fixity('free', np.zeros(self._ndf, int))
        newNode = self._activeNodeType(x, fixity, label)  # either 2D or 3D depending on the dimension type.
        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].label = label
            return 0
        else:
            self._addNewNode(newNode, sort)
            return 1
        return -1

    def _addNewNode(self, newNode: Node2D, sort: bool = True):
        self.Nnodes += 1
        newNode._setID(self.Nnodes)
        self.nodes.append(newNode)
        self.nodeCoords.add(newNode.x)
        if sort:
            self._sortNodes()

    def addNodes(self, xCoords: list[float],
                 fixities: list[Union[list, str, Fixity]] = None,
                 labels: list[str] = None):


        newNoads = len(xCoords)
        if fixities == None:
            fixity = Fixity('free', np.zeros(self._ndf, int))
            fixities = [fixity] * newNoads

        if labels is None:
            labels = [None] * newNoads

        sort = False  # only sort at the end!
        for ii in range(newNoads):
            self.addNode(xCoords[ii], fixities[ii], labels[ii], sort)

        self._sortNodes()

    def _checkfixityInput(self, fixity: Fixity):


        fixVals = fixity.fixityValues
        if set(fixVals).issubset({0, 1}) != True:
            raise ValueError("Fixity must be a list of zeros and ones.")

        # I forget why I explicitly check for 2 here.
        # I'd guess we're runing out if just one value is provided
        if (len(fixVals) == 2 or len(fixVals) > self._ndf):
            raise ValueError(f"Fixity must be a integer or vector of length {self._ndf}")

    def _convertFixityInput(self, fixity):


        if isinstance(fixity, int):
            return [fixity] * self._ndf
        else:
            return fixity

    def setFixity(self, x: float, fixity: list[Union[list, Fixity]],
                  label=None):


        fixity = self._convertFixityInput(fixity)
        fixity = _convertFixityInput2D(fixity)
        self._checkfixityInput(fixity)

        if x in self.nodeCoords:
            index = self._findNode(x)
            self.nodes[index].fixity = fixity
            self.nodes[index].hasReaction = True
            if label:
                self.nodes[index].label = label
        else:
            self.addNode(x, fixity, label)

    def addPointLoad(self, x: float, pointLoad: list, label: str = '',
                     labelNode=False):


        # Catch incorrectly given types.
        if hasattr(pointLoad, '__iter__') == False:
            raise Exception('Point load vector must be a list or Numpy array.')

        # Converty to np array. We do vector operations on data downstream
        if isinstance(pointLoad, list):
            pointLoad = np.array(pointLoad)

        loadID = len(self.pointLoads) + 1

        # Check if the node exists, add it if not.
        if x in self.nodeCoords:
            nodeIndex = self._findNode(x)
        else:
            self.addNode(x)
            nodeIndex = self._findNode(x)

        # index is what is used to look up, use one greater for the
        self.nodes[nodeIndex].pointLoadIDs.append(loadID)
        if labelNode:
            self.nodes[nodeIndex].label = label

        nodeID = nodeIndex + 1
        newLoad = PointLoad(pointLoad, x, nodeID, label)
        self.pointLoads.append(newLoad)

    def addVerticalLoad(self, x: float, Py: float, label: str = '', labelNode=False):

        if self._ndf == 3:
            pointLoad = np.array([0., Py, 0.])
        elif self._ndf == 6:
            pointLoad = np.array([0., Py, 0., 0., 0., 0.])

        self.addPointLoad(x, pointLoad, label, labelNode)

    # !!! TODO:
    # State which direction positive is.
    def addMoment(self, x: float, M: float, label: str = '', labelNode=False):


        if self._ndf == 3:
            pointLoad = np.array([0., 0., M])
        elif self._ndf == 6:
            pointLoad = np.array([0., 0., 0., 0., 0., M])

        self.addPointLoad(x, pointLoad, label, labelNode)

    def addHorizontalLoad(self, x: float, Px: float, label: str = '', labelNode=False):


        if self._ndf == 3:
            pointLoad = np.array([Px, 0., 0.])
        elif self._ndf == 6:
            pointLoad = np.array([Px, 0., 0., 0., 0., 0.])

        self.addPointLoad(x, pointLoad, label, labelNode)

        # TODO: use a dictionary to speed this process up?!

    def _findNode(self, xInput: float):


        for ii, node in enumerate(self.nodes):
            if xInput == node.x:
                return ii
        return None

    def addDistLoad(self, x1: float, x2: float, distLoad: float, label: str = ''):


        defaultFixity = np.zeros(self._ndf, int)
        distLoad = np.array(distLoad)

        if x1 not in self.nodeCoords:
            self.addNode(x1, defaultFixity)
        if x2 not in self.nodeCoords:
            self.addNode(x2, defaultFixity)

        newEleLoad = EleLoadDist(x1, x2, distLoad, label)
        self.eleLoads.append(newEleLoad)

    def addDistLoadVertical(self, x1: float, x2: float, qy: float, label: str = ''):


        if self._ndf == 3:
            distLoad = np.array([0., qy])
        if self._ndf == 6:
            distLoad = np.array([0., qy, 0.])
        self.addDistLoad(x1, x2, distLoad, label)

    def addDistLoadHorizontal(self, x1: float, x2: float, qx: float, label: str = ''):


        if self._ndf == 3:
            distLoad = np.array([qx, 0.])
        if self._ndf == 6:
            distLoad = np.array([qx, 0., 0.])
        self.addDistLoad(x1, x2, distLoad, label)

    def addLinLoad(self, x1: float, x2: float, linLoad: list[list], label: str = ''):


        defaultFixity = np.zeros(self._ndf, int)
        linLoad = np.array(linLoad)

        if x1 not in self.nodeCoords:
            self.addNode(x1, defaultFixity)
        if x2 not in self.nodeCoords:
            self.addNode(x2, defaultFixity)

        newEleLoad = EleLoadLinear(x1, x2, linLoad, label)
        self.eleLoads.append(newEleLoad)


    def addLinLoadVertical(self, x1: float, x2: float, qy: list[float], label: str = '',
                           **kwargs):


        self._checkForOutOfDateKwargs(kwargs)

        if self._ndf == 3:
            linLoad = np.array([[0., 0.], qy])
        if self._ndf == 6:
            linLoad = np.array([[0., 0.], qy, [0., 0.]])
        self.addLinLoad(x1, x2, linLoad, label)

    def addLinLoadHorizontal(self, x1: float, x2: float, qx: list[float], label: str = ''):


        if self._ndf == 3:
            linLoad = np.array([qx, [0., 0.]])
        if self._ndf == 6:
            linLoad = np.array([qx, [0., 0.], [0., 0.]])

        self.addLinLoad(x1, x2, linLoad, label)

    def Fmax(self, index):

        Fmax = 0
        Fmin = 0
        for node in self.nodes:
            F1 = node.Fint[index]
            F2 = node.Fint[index + self._ndf]

            if F1 < Fmin or F2 < Fmin:
                Fmin = min(F1, F2)

            if Fmax < F1 or Fmax < F2:
                Fmax = max(F1, F2)
        return Fmin, Fmax

    def getNodes(self):
        return self.nodes


class EulerBeam(Beam):

    def __init__(self, xcoords: list = None, fixities: list = None, labels: list = None,
                 section=None, dimension='2D'):
        # geomTransform has values 'Linear' or 'PDelta'
        self._initArrays()
        self._initDimensionVariables(dimension)
        self.nodes = []
        self.eleLoads = []

        if xcoords is None:
            xcoords = []
        if fixities is None:
            fixities = []
        if labels is None:
            labels = []
        if section is None:
            section = SectionBasic()

        NnewNodes = len(xcoords)
        fixities = self._initFixities(fixities, NnewNodes)

        if len(labels) == 0:
            labels = [None] * NnewNodes

        if len(xcoords) != 0:
            self.addNodes(xcoords, fixities, labels)

        self.section = section
        self.d = 1
        self.plotter = None
        self.EleType = 'elasticBeamColumn'

    def _parseCoords(self, xcoords):
        if type(xcoords) == float:
            xcoords = [xcoords]
        if len(xcoords) == 1:
            xcoords = [0] + xcoords

    def _initFixities(self, fixities, NnewNodes):
        if len(fixities) == 0:
            name = FixityTypes2D.releaseNames[0]
            fixities = [Fixity(name, np.zeros(self._ndf))] * NnewNodes
        if len(fixities) != NnewNodes:
            raise Exception('A fixity must be provided for each node.')
        return fixities

    def getMaterialPropreties(self):

        if self._dimension == '2D':
            return [self.section.E, self.section.G,
                    self.section.A, self.section.Iz]
        elif self._dimension == '3D':
            # Area, E_mod, G_mod, Jxx, Iy, Iz,
            return [self.section.E, self.section.G, self.section.A,
                    self.section.Iz, self.section.Iy, self.section.J]

    def getBMD(self) -> list[list[float], list[float]]:

        if self._dimension == '2D':
            M = self.getInternalForce(2)
        elif self._dimension == '3D':
            M = self.getInternalForce(5)
        return M

    def getSFD(self):

        return self.getInternalForce(1)

    def getInternalForce(self, index):


        xcoords = np.zeros(self.Nnodes * 2)
        force = np.zeros(self.Nnodes * 2)
        for ii, node in enumerate(self.nodes):
            ind1 = 2 * ii
            ind2 = ind1 + 2
            xcoords[ind1:ind2] = node.x
            force[ind1:ind2] = node.getInternalForces(index)
        return xcoords, force

    @property
    def Mmax(self):
        return self.Fmax(2)

    @property
    def Vmax(self):
        return self.Fmax(1)

    @property
    def reactions(self):
        reactions = []
        for node in self.nodes:
            if node.hasReaction:
                reactions.append(node.rFrc)
        return reactions

    @property
    def reactionDict(self):
        reactions = {}
        for node in self.nodes:
            if node.hasReaction:
                reactions[node.x] = node.rFrc
        return reactions


def newEulerBeam(x2, x1=0, meshSize=101, section=None, dimension='2D'):

    if x2 <= x1:
        raise Exception('x2 must be greater than x1')

    x = np.linspace(x1, x2, meshSize)
    return EulerBeam(x, section=section, dimension=dimension)


def newSimpleEulerBeam(x2, x1=0, meshSize=101, q=0, section=None, dimension='2D'):

    if x2 <= x1:
        raise Exception('x2 must be greater than x1')

    x = np.linspace(x1, x2, meshSize)

    beam = EulerBeam(x, dimension='2D', section=section)
    beam.addNode(x1, [1, 1, 0])
    beam.addNode(x2, [0, 1, 0])
    if q != 0:
        beam.addDistLoadVertical(x1, x2, q)
    return beam


class BasicOptionsDiagram:
    def __init__(self, scale=1, supScale=0.8):


        self.lw = 1 * scale
        self.scale = scale  # Scales all drawing elements
        self.supScale = supScale  # Scales all drawing elements

        # Beam Propreties
        self.lw_beam = 2 * scale
        self.c_beam = 'black'

        # Point Load Propreties
        self.w_PointLoad = 0.03 * scale
        self.c_PointLoad = 'C0'
        self.c_PointLoadDist = 'grey'
        # changes the offset from the point in x/y
        self.labelOffset = 0.1 * scale

        # Pin support geometry variables
        self.r = 0.08 * scale * supScale
        self.hTriSup = 0.3 * scale * supScale
        self.wTriSup = 2 * self.hTriSup

        # Parameters for the rectangle below the pin support
        self.hFixedRect = 0.2 * scale * supScale
        self.marginFixedSup = 0.2 * scale * supScale
        self.hatch = '/' * int((3 / (scale * supScale)))
        self.wRect = self.wTriSup + self.marginFixedSup

        self.lineOffset_roller = self.hFixedRect / 10
        self.hRollerGap = self.hFixedRect / 4
        self.y0 = 0

        # Point Load
        self.lw_pL = 0.03 * scale  # The width of the
        # self.lw_pLbaseWidth = 0.01 * scale # The width of the
        self.arrowWidth = 5 * self.lw_pL

        # Moment Point Load
        self.r_moment = 0.15
        self.rotationAngle = 30
        self.c_moment = 'C0'

        # Distributed Load Propreties
        self.c_dist_bar = 'grey'
        self.spacing_dist = (1 / 20)
        self.barWidth = 1.2 * scale

        self.lw_pL_dist = 0.015
        self.arrowWidth_pL_dist = 5 * self.lw_pL_dist

        # Linear Distributed Load Options
        self.minLengthCutoff = 0.075 * self.scale

        # label Options
        self.labelOffset = 0.1 * scale
        self.textSize = 12 * scale

    def getSupportDiagramOptions(self):
        args = [self.lw, self.scale, self.supScale,
                self.r, self.hTriSup, self.wTriSup, self.hFixedRect,
                self.marginFixedSup, self.hatch, self.wRect,
                self.lineOffset_roller,
                self.hRollerGap, self.y0]

        return supportDiagramOptions(*args)

    def getPointLoadOptions(self):
        args = [self.lw_pL, self.c_PointLoad, self.arrowWidth]
        return PointLoadOptions(*args)

    def getPointLoadDistOptions(self):
        args = [self.lw_pL_dist, self.c_dist_bar, self.arrowWidth_pL_dist]
        return PointLoadOptions(*args)

    def getMomentPointLoadOptions(self):
        args = [self.lw_pL, self.c_moment, self.arrowWidth, self.r_moment,
                self.rotationAngle]

        return MomentPointLoadOptions(*args)

    def getDistLoadOptions(self):
        args = [self.lw, self.c_dist_bar, self.arrowWidth, self.spacing_dist,
                self.barWidth]

        return DistLoadOptions(*args)

    def getLinLoadOptions(self):
        args = [self.lw, self.c_dist_bar, self.arrowWidth, self.spacing_dist,
                self.barWidth, self.minLengthCutoff]

        return LinLoadOptions(*args)

    def getLabelOptions(self):
        args = [self.labelOffset, self.textSize]

        return LabelOptions(*args)

    def getBeamOptions(self):
        args = [self.lw_beam, self.c_beam]
        return BeamOptions(*args)
