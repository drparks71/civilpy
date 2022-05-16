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
import matplotlib.pyplot as plt
import textalloc as ta
import numpy as np

from .baseclasses import Beam, Node2D
from .loads import EleLoadBox
from .baseclasses import EleLoadDist, EleLoadLinear
from .configure import diagramUnits
from .plot import BasicDiagramPlotter


class BeamPlotter2D:
    def __init__(self, beam, figsize=8, units='environment'):


        self.beam = beam
        self.figsize = figsize

        if units == 'environment':
            self.unitHandler = diagramUnits.activeEnv
        else:
            self.unitHandler = diagramUnits.getEnvironment(units)

        L = beam.getLength()
        xscale = L / self.figsize
        self.xscale = xscale
        baseSpacing = self.beam.getLength() / self.xscale

        self.plotter: BasicDiagramPlotter = BasicDiagramPlotter(L=L)
        self.plotter.setEleLoadLineSpacing(baseSpacing)

        xlims = beam.getxLims()
        self.xmin = xlims[0]
        self.xmax = xlims[0]

        self.xlimsPlot = [(xlims[0] - L / 20) / xscale, (xlims[1] + L / 20) / xscale]

        self.ylimsPlot = [-L / 10 / xscale, L / 10 / xscale]

        self.plottedNodeIDs = []

    def plot(self, plotLabel=False, labelForce=True,
             plotForceValue=True, **kwargs):

        args = (self.figsize, self.xlimsPlot, self.ylimsPlot)
        self.fig, self.ax = self.plotter._initPlot(*args)
        self.plotSupports()

        pfplot, efplot = None, None
        if self.beam.pointLoads:
            pfplot = self.plotPointForces()
        if self.beam.pointLoads and plotLabel:
            self.plotPointForceLables(pfplot, labelForce, plotForceValue)
        if self.beam.eleLoads:
            efplot, xcoords = self.plotEleForces()
        if self.beam.eleLoads and plotLabel:
            self.plotDistForceLables(efplot, xcoords, labelForce, plotForceValue)

        if plotLabel:
            self.plotLabels()

        self.plotBeam()

        if (not (pfplot is None)) or (not (efplot is None)):
            self._adjustPlot(pfplot, efplot)

    def _adjustPlot(self, pfplot, efplot):
        if (pfplot is None):
            pfplot = (0)
        if (efplot is None):
            efplot = (0)

        fmax = max(np.max(pfplot), np.max(efplot))
        fmin = min(np.min(pfplot), np.min(efplot))
        if fmin < self.ylimsPlot[0]:
            self.ylimsPlot[0] = fmin
        if self.ylimsPlot[1] < fmax:
            self.ylimsPlot[1] = fmax

        self.ax.set_ylim(self.ylimsPlot)

    def plotBeam(self):

        xlims = self.beam.getxLims()
        xy0 = [xlims[0] / self.xscale, 0]
        xy1 = [xlims[1] / self.xscale, 0]
        self.plotter.plotBeam(self.ax, xy0, xy1)

    def plotSupports(self):


        for node in self.beam.nodes:
            fixityType = node.getFixityType()
            x = node.getPosition()
            xy = [x / self.xscale, 0]


            kwargs = {}
            if fixityType == 'fixed' and x == self.xmin:
                kwargs = {'isLeft': True}

            if fixityType == 'fixed' and not x == self.xmin:
                kwargs = {'isLeft': False}

            self.plotter.plotSupport(self.ax, xy, fixityType, kwargs)

    def _addLabelToPlotted(self, nodeID):
        self.plottedNodeIDs.append(nodeID)

    def _checkIfLabelPlotted(self, nodeID):
        check = nodeID in self.plottedNodeIDs
        return check

    def plotLabels(self):


        for node in self.beam.nodes:
            label = node.label
            x = node.getPosition()

            if label and (self._checkIfLabelPlotted(node.ID) != True):
                xy = [x / self.xscale, 0]
                self.plotter.plotLabel(self.ax, xy, label)
                self._addLabelToPlotted(node.ID)

    def _getValueText(self, diagramType, forceValue):

        unit = self.unitHandler[diagramType].unit
        scale = self.unitHandler[diagramType].scale
        Ndecimal = self.unitHandler[diagramType].Ndecimal

        # Round force
        forceValue *= scale
        if Ndecimal == 0:
            forceValue = round(forceValue)
        else:
            forceValue = round(forceValue * 10 ** Ndecimal) / 10 ** Ndecimal
        return forceValue, unit

    def plotPointForceLables(self, fplot, labelForce, plotForceValue):


        inds = range(len(self.beam.pointLoads))
        for ii, force in zip(inds, self.beam.pointLoads):
            Px, Py, Mx = fplot[ii]
            isMoment = False
            if Mx != 0:
                isMoment = True
                Py = -0.15
                diagramType = 'moment'
                fText = force.P[2]
            else:
                # shift the force down so it fits in the diagram!
                Py += 0.15
                diagramType = 'force'
                fText = np.sum(force.P[:2] ** 2) ** 0.5

            # get the label from the node - it's store there and not on the force.
            labelBase = force.label
            # labelBase = self.beam.nodes[force.nodeID - 1].label
            label = ''

            if labelBase and labelForce and isMoment:
                label += f'$M_{{{labelBase}}}$'  # Tripple brackets needed to make the whole thing subscript

            elif labelBase and labelForce and (not isMoment):
                label += f'$P_{{{labelBase}}}$'
            else:
                pass

            if labelBase and plotForceValue and labelForce:
                valueText, unit = self._getValueText(diagramType, fText)
                label += ' = ' + str(valueText) + "" + unit

            x = force.getPosition()
            xy = [x / self.xscale, -Py]

            if label and self._checkIfLabelPlotted(force.nodeID) != True:
                self.plotter.plotLabel(self.ax, xy, label)
                self._addLabelToPlotted(force.nodeID)

    def plotDistForceLables(self, fplot, xcoords, labelForce, plotForceValue):

        diagramType = 'distForce'
        inds = range(len(self.beam.eleLoads))
        for ii, force in zip(inds, self.beam.eleLoads):
            qx, qy = fplot[ii]
            fText = force.P[1]

            labelBase = force.label
            label = ''

            if labelBase and labelForce:
                label += f'$q_{{{labelBase}}}$'

            if labelBase and plotForceValue and labelForce:
                valueText, unit = self._getValueText(diagramType, fText)
                label += ' = ' + str(valueText) + "" + unit

            x1, x2 = xcoords[ii]
            aMid = (x1 + x2) / 2
            xy = [aMid, -qy]  # note, aMid has already been scaled
            self.plotter.plotLabel(self.ax, xy, label)

    def _getForceVectorLengthPoint(self, forces, vectScale=1):

        fscale0 = 0.4
        fstatic0 = 0.3

        # Normalize forces
        forces = np.array(forces)
        signs = np.sign(forces)

        # The maximum force in each direction
        Fmax = np.max(np.abs(forces), 0)

        # Avoid dividing by zero later
        Inds = np.where(np.abs(Fmax) == 0)
        Fmax[Inds[0]] = 1

        # Find all force that are zero. These should remain zero
        Inds0 = np.where(np.abs(forces) == 0)

        # Plot the static portion, and the scale port of the force
        fscale = fscale0 * abs(forces) / Fmax
        fstatic = fstatic0 * np.ones_like(forces)
        fstatic[Inds0[0], Inds0[1]] = 0

        fplot = (fscale + fstatic) * signs

        return fplot * vectScale

    def plotPointForces(self):

        forces = []
        xcoords = []
        for force in self.beam.pointLoads:
            forces.append(force.P)
            xcoords.append(force.x / self.xscale)
        fplot = self._getForceVectorLengthPoint(forces)
        NLoads = len(forces)

        for ii in range(NLoads):
            Px, Py, Mx = fplot[ii]
            x = xcoords[ii]
            if (Px == 0 and Py == 0):  # if it's a moment, plot it as a moment
                if Mx < 0:
                    postive = True
                else:
                    postive = False
                self.plotter.plotPointMoment(self.ax, (x, 0), postive)
            else:
                self.plotter.plotPointForce(self.ax, (x - Px, -Py), (Px, Py))

        return fplot

    def _plotEleForce(self, box: EleLoadBox):

        Py = box.fout

        if (Py[0] == 0) and (Py[1] == 0):
            print("WARNING: Plotted load has no vertical component.")

        if box.isConstant:
            self.plotter.plotElementDistributedForce(self.ax, box)
        else:
            self.plotter.plotElementLinearForce(self.ax, box)

    def normalizeData(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    def _getLinFint(self, Ptmp):


        # fintTemp = list(self.normalizeData(Ptmp))
        # If both are on the positive side
        if 0 < np.sign(Ptmp[0]) and 0 < np.sign(Ptmp[1]):

            if Ptmp[0] < Ptmp[1]:
                fintTemp = [Ptmp[0] / Ptmp[1], 1]
            elif Ptmp[0] == Ptmp[1]:  # If equal the load acts like a constant load
                fintTemp = [1, 1]
            else:
                fintTemp = [1, Ptmp[1] / Ptmp[0]]
            Ptmp = [0, max(Ptmp)]

        # If both are on the negative side side
        elif np.sign(Ptmp[0]) < 0 and np.sign(Ptmp[1]) < 0:

            if Ptmp[0] < Ptmp[1]:
                fintTemp = [0, Ptmp[1] / Ptmp[0]]
            elif Ptmp[0] == Ptmp[1]:  # If equal the load acts like a constant load
                fintTemp = [0, 0]
            else:
                fintTemp = [1 - Ptmp[0] / Ptmp[1], 0]
            Ptmp = [min(Ptmp), 0]

        # If the inputs change sign, just use the normalized value.
        else:
            fintTemp = list(self.normalizeData(Ptmp))
        return Ptmp, fintTemp

    def _getEleForceBoxes(self):


        eleBoxes = []

        for load in self.beam.eleLoads:
            xDiagram = [load.x1 / self.xscale, load.x2 / self.xscale]

            if isinstance(load, EleLoadDist):  # Constant Load
                # Adapt the load so it's a 2D vector
                Ptmp = [0, -load.P[1]]  # !!! The sign is flipped to properly stack
                if -load.P[1] < 0:  # !!! The sign is flipped to properly stack
                    fintTemp = [0, 0]  # start at the bottom if negative
                else:
                    fintTemp = [1, 1]  # start at the top if negative
                eleBoxes.append(EleLoadBox(xDiagram, Ptmp, fintTemp))
            # Arbitary Distributed Load between two points
            elif isinstance(load, EleLoadLinear):
                Ptmp = -load.P[1]  # !!! The sign is flipped to properly stack

                Ptmp, fintTemp = self._getLinFint(Ptmp)
                eleBoxes.append(EleLoadBox(xDiagram, Ptmp, fintTemp))

        eleBoxes = _setForceVectorLengthEle(eleBoxes, vectScale=0.4)
        stacker = Boxstacker(eleBoxes)
        eleBoxes = stacker.setStackedDatums()

        return eleBoxes

    def plotEleForces(self):


        eleBoxes = self._getEleForceBoxes()
        for box in eleBoxes:
            self._plotEleForce(box)

        fplot = [box.y for box in eleBoxes]
        xcoords = [box.x for box in eleBoxes]

        return fplot, xcoords


def plotBeamDiagram(beam, plotLabel=True, labelForce=False,
                    plotForceValue=False, units='environment'):
    diagram = BeamPlotter2D(beam, units=units)
    diagram.plot(plotLabel, labelForce, plotForceValue)
    return diagram.fig, diagram.ax


def plotMoment(beam: Beam, scale: float = -1, yunit='Nm', **kwargs):
    ind = beam.getDOF() - 1
    return plotInternalForce(beam, ind, scale, yunit=yunit, **kwargs)


def plotShear(beam: Beam, scale: float = 1, **kwargs):
    return plotInternalForce(beam, 1, scale, **kwargs)


def _getForceValues(beam, index):
    Nnodes = len(beam.nodes)
    xcoords = np.zeros(Nnodes * 2)
    force = np.zeros(Nnodes * 2)
    labels = [None] * Nnodes
    for ii, node in enumerate(beam.nodes):
        ind1 = 2 * ii
        ind2 = ind1 + 2
        xcoords[ind1:ind2] = node.x
        force[ind1:ind2] = node.getInternalForces(index)
        labels[ii] = node.label

    return xcoords, force, labels


def _initOutputFig(showAxis, showGrid):
    fig, ax = plt.subplots(dpi=300)

    if not showAxis:
        ax.axis("off")
    else:
        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        ax.spines['left'].set_linewidth(0)
        ax.spines['bottom'].set_linewidth(0)

    if showGrid:
        ax.grid(which='major', axis='both', c='black', linewidth=0.4)
        ax.minorticks_on()
        ax.tick_params(axis='y', which='minor', colors='grey')
        ax.grid(which='minor', axis='both', c='grey')

    return fig, ax


def _plotAxis(ax, xcoords, xunit, yunit, baseY='Internal Force'):
    plt.plot([xcoords[0], xcoords[-1]], [0, 0], c='black', linewidth=0.5)

    xlabel = 'Distance (' + xunit + ')'
    ylabel = baseY + '  (' + yunit + ')'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def _plotLabels(ax, xcoords, ycoords, labels):
    offsetx = (max(xcoords) - min(xcoords)) / 100
    offsety = (max(ycoords) - min(ycoords)) / 50
    for ii in range(len(labels)):
        xcoord = xcoords[ii]
        label = labels[ii]
        if label is not None:
            _plotLabel(ax, xcoord, label, offsetx, offsety)


def _plotLabel(ax, xcoord, label, offsetx, offsety):
    x = xcoord + offsetx
    y = 0 + offsety
    ax.text(x, y, label)


def _valsInPercentTol(y1, y2, tolPercent = 10e-4):
    if abs((y1/y2) - 1) < tolPercent:
        return True
    return False


def _get_discontinuity_inds(force, tol=1e-6):
    tolMin = 1e-6
    force2D = force.reshape(-1, 2)
    absDiff = np.abs(np.diff(force2D))
    # small changes won't be counted
    # If there are no discontinities then cap the change to detect no points.
    diffTol = max(np.max(absDiff) * tol, tol)

    indDisTmp = np.where(diffTol < np.abs(np.diff(force2D)))[0]
    indDisTmp = np.concatenate((indDisTmp * 2, indDisTmp * 2 + 1))
    # indDis      = indDisTmp[1:-1]
    return indDisTmp


def _getLabelInds(xcoords: list, force: list, labels: list):
    nonNoneLabels = np.array(labels) != None
    nonEmptyLabels = np.array(labels) != ''

    indLabelTmp = np.where(nonNoneLabels * nonEmptyLabels)[0]

    indLabelTmp = indLabelTmp * 2
    indLabelTmp = np.array([indLabelTmp, indLabelTmp + 1]).T

    # If the label index is at a discontinous point, get both sides of the point.
    indLabel = []
    tol = 10e-6
    for ind1, ind2 in indLabelTmp:
        xcoordEqual = (xcoords[ind1] == xcoords[ind2])
        ycoordUnequal = tol < abs(force[ind1] / force[ind2] - 1)
        if xcoordEqual and ycoordUnequal:
            indLabel += [ind1, ind2]
        else:
            indLabel.append(ind1)
    return indLabel


def _getLabelIndsDisp(xcoords: list, force: list, labels: list):
    nonNoneLabels = np.array(labels) != None
    nonEmptyLabels = np.array(labels) != ''

    indLabelTmp = np.where(nonNoneLabels * nonEmptyLabels)[0]
    indLabel = np.array(indLabelTmp, dtype=int)

    return indLabel


def _getPOIIndsForce(xcoords, ycoords, labels, ycordsSecondary, poiOptions):
    # Get Label Inds
    indLabel = []
    if poiOptions['showLabels'] == True:
        indLabel = _getLabelInds(xcoords, ycoords, labels)

    # Get Discontinuity Indicies
    indDis = []
    if poiOptions['showDiscontinutiy'] == True:
        indDis = _get_discontinuity_inds(ycoords)

    # If it's a moment plot, catch points of shear discontinuty.
    indDisShear = []
    if ycordsSecondary is not None:
        indDisShear = _get_discontinuity_inds(ycordsSecondary)

    # Get Max/min Indicies
    maxMinInds = []
    if poiOptions['showMax'] == True:
        indMax = np.argmax(ycoords)
        indMin = np.argmin(ycoords)
        maxMinInds = [indMax, indMin]

    return np.concatenate((indDis, indDisShear, np.array(indLabel, dtype=int), maxMinInds))


def _processPOIDictInputs(poiOptions):
    if 'showLabels' not in poiOptions:
        poiOptions['showLabels'] = True

    if 'showDiscontinutiy' not in poiOptions:
        poiOptions['showDiscontinutiy'] = True

    if 'showMax' not in poiOptions:
        poiOptions['showMax'] = True

    return poiOptions


def valRelativelyNearZero(val, referenceMax, tolPercent = 10e-9):
    return (abs(val / referenceMax) < tolPercent)


def _findCloseDiscontinousPoints(force, ind, poiInd):
    # Combine discontinuous points that are within a tolerance of eachother
    leftAdjecentPointExists = False
    for indOther in poiInd:
        if (indOther - 1 == ind):
            leftAdjecentPointExists = True
            break

    # don't add the point if it is next to another point and close in value
    if leftAdjecentPointExists and _valsInPercentTol(force[ind], force[indOther]):
        return True
    else:
        return False


def removeFalsePOI(candidatePOI, force) -> list[int]:

    # get the forces again
    absMax = np.max(np.abs(force))

    # remove the end points. These aren't interesting
    end = len(force) - 1
    start = 0
    if end in candidatePOI:
        candidatePOI.remove(end)
    if start in candidatePOI:
        candidatePOI.remove(start)

    # make a list of the second from last points.
    # If these are close to zero we will remove them later.
    candidateEndPoints = [1, len(force) - 2]

    filteredPoiInd = []
    poiInd = [int(ind) for ind in candidatePOI]
    for ind in poiInd:
        ind = int(ind)

        if _findCloseDiscontinousPoints(force, ind, poiInd):
            continue

        # Values
        if ind in candidateEndPoints and valRelativelyNearZero(force[ind], absMax):
            continue

        filteredPoiInd.append(ind)
    filteredPoiInd = set(filteredPoiInd)
    return filteredPoiInd


def _getPOIIndsDisp(xcoords, ycoords, labels, ycordsSecondary, poiOptions):

    # Get Label Inds
    indLabel = []
    if poiOptions['showLabels'] == True:
        indLabel = _getLabelIndsDisp(xcoords, ycoords, labels)

    # Get Max/min Indicies
    maxMinInds = []
    if poiOptions['showMax'] == True:
        indMax  = np.argmax(ycoords)
        indMin  = np.argmin(ycoords)
        maxMinInds = [indMax, indMin]

    return np.concatenate((np.array(indLabel, dtype=int), maxMinInds))


def findAllPOI(xcoords, ycoords, labels, ysecondary=None, POIOptions: dict = None):

    # Prevent the options from having no value.
    if POIOptions == None:
        POIOptions = {}

    # add default values if they aren't included
    POIOptions = _processPOIDictInputs(POIOptions)

    # Check if the
    if len(ycoords) == len(labels):
        union = _getPOIIndsDisp(xcoords, ycoords, labels, ysecondary, POIOptions)
    else:
        union = _getPOIIndsForce(xcoords, ycoords, labels, ysecondary, POIOptions)

    # poiInd  = list(union)
    poiInd = [int(ind) for ind in union]
    return poiInd


def plotPOI(fig, ax, xcoords, force, labels, filteredPoiInd):
    labelX = []
    labelY = []
    labelText = []
    for ind in filteredPoiInd:
        labelName = labels[int((ind + 1) / 2)]
        x0 = xcoords[ind]
        y0 = force[ind]
        xOut = round(x0, 2)
        yOut = round(y0, 1)
        base = ''
        if labelName:
            base = ' Point ' + labelName + ' \n'
        textX = f' x = {xOut} \n'
        textY = f' y = {yOut} '
        text = base + textX + textY
        labelX.append(x0)
        labelY.append(y0)
        labelText.append(text)

    ta.allocate_text(fig, ax, labelX, labelY, labelText, textsize=8,
                     x_scatter=labelX, y_scatter=labelY,
                     x_lines=[xcoords], y_lines=[force],
                     linecolor='grey', linewidth=0.5,
                     max_distance=0.5, min_distance=0.02,
                     seed=1, )


def plotInternalForce(beam: Beam, index: int, scale: float, xunit='m', yunit='N',
                      showAxis=True, showGrid=False, labelPlot=True,
                      labelPOI=False, POIOptions=None):
    xcoords, force, labels = _getForceValues(beam, index)
    forceScaled = force * scale

    fig, ax = _initOutputFig(showAxis, showGrid)
    _plotAxis(ax, xcoords, xunit, yunit)

    if labelPlot:
        _plotLabels(ax, xcoords[::2], forceScaled, labels)
    line = plt.plot(xcoords, forceScaled)

    if labelPOI:
        shear = None
        if index == 2:
            _, shear, _ = _getForceValues(beam, index - 1)
        candidatePOI = findAllPOI(xcoords, forceScaled, labels, shear, POIOptions)
        filteredPoiInd = removeFalsePOI(candidatePOI, force)
        plotPOI(fig, ax, xcoords, forceScaled, labels, filteredPoiInd)

    return fig, ax, line


def _checkInRange(xrange1, xrange2):
    if (xrange2[0] <= xrange1[1]) and (xrange1[0] <= xrange2[1]):
        return True
    else:
        return False


def checkBoxesForOverlap(box1: EleLoadBox, box2: EleLoadBox):

    if _checkInRange(box1.x, box2.x) and _checkInRange(box1.y, box2.y):
        return True
    else:
        return False


class Boxstacker:

    def __init__(self, boxes: list[EleLoadBox]):

        self.boxes = boxes

    def setStackedDatums(self):


        boxes = self.boxes
        Nforces = len(boxes)
        lengths = [None] * Nforces
        xcoords = np.array([box.x for box in boxes])
        ycoords = np.array([box.y for box in boxes])  # [bottom, top]

        # Get the lengths, the start with the longest and go to shortest
        lengths = xcoords[:, 1] - xcoords[:, 0]
        sortedInds = np.argsort(lengths)[::-1]

        # the current x and y points being plotted.
        posStackx = []
        posStackTop = []
        negStackx = []
        negStackTop = []

        # start at the widest items and plot them first
        for ind in sortedInds:
            box = boxes[ind]

            # Datum is where we point towards!
            y = ycoords[ind]
            x = xcoords[ind]

            # Case 1: Constantly distributed, use dy
            if box.isConstant:
                dy = box.fout[0]

                if 0 < dy:
                    self._addToStack(box, dy, x, posStackx, posStackTop)
                else:
                    self._addToStack(box, dy, x, negStackx, negStackTop)

                    # Case 2: linearly distributed, no sign change, use max values
            elif not box.changedDirection:
                # If a value is greater than zero, stack on pos side.
                if 0 < max(y):
                    dy = max(y)
                else:
                    dy = min(y)

                if 0 < dy:
                    self._addToStack(box, dy, x, posStackx, posStackTop)
                else:
                    self._addToStack(box, dy, x, negStackx, negStackTop)

            # Case 3: Linearly distributed through zero, we work with fout
            # print(box.changedDirection)
            elif box.changedDirection:
                inPos, _ = self._checkInStack(x, posStackx)
                inNeg, _ = self._checkInStack(x, negStackx)

                # If
                dyPos = max(box.fout)
                dyNeg = min(box.fout)

                # Case 3i:
                # If there is no stacks, add it to the bottom of both stacks
                if (not inPos) and (not inNeg):
                    self._addToStack(box, dyPos, x, posStackx, posStackTop)
                    self._addToStack(box, dyNeg, x, negStackx, negStackTop)

                # Case 3ii:
                # If there is a positive stack add it to the top of that stack
                elif inPos:
                    dy = dyPos - dyNeg
                    dDatum = -dyNeg

                    self._addToStack(box, dy, x, posStackx, posStackTop, dDatum)
                # Case iii:
                # If there is only negative, shift above the x axis
                elif inNeg:
                    # box.shiftDatum(-box.datum)
                    dDatum = -dyNeg
                    dy = -dyNeg
                    self._addToStack(box, dy, x, posStackx, posStackTop, dDatum)

        return boxes

    def _checkIfInRange(self, xtest, x1, x2):
        if (x1 < xtest) and (xtest < x2):
            return True
        return False

    def _addToStack(self, box, dy, xcoords, stackx, stacktops, dDatum=0):
        y0 = self._getStackTop(xcoords, stackx, stacktops)
        box.shiftDatum(y0 + dDatum)
        stackx.append(xcoords)
        stacktops.append((y0 + dy))

    def _checkInStack(self, xCurrent: list[float, float],
                      stackRanges: list[list[float, float]]):


        # Check all the stacks to see if the current stack is
        inStack = False
        Nloads = len(stackRanges)
        for ii in range(Nloads):
            localInd = Nloads - 1 - ii
            x1, x2 = stackRanges[localInd]
            if self._checkIfInRange(xCurrent[0], x1, x2):  # left side
                return True, localInd
            if self._checkIfInRange(xCurrent[1], x1, x2):  # right side
                return True, localInd

            # Stack boxes that are directly on top of eachother.
            # We need both to be true so boxes side by side do not stack
            if (xCurrent[0] == x1) and (xCurrent[1] == x2):  # right side
                return True, localInd
        return inStack, None

    def _getStackTop(self, xCurrent: list[float, float],
                     stackRanges: list[list[float, float]],
                     currentY: list[list[float, float]]):


        inStack, localInd = self._checkInStack(xCurrent, stackRanges)
        if inStack == True:
            return currentY[localInd]

        return 0


def _getSigns(forces):
    tmpForces = np.copy(forces)
    inds = np.where(tmpForces == 0)
    tmpForces[inds] = 1
    signs = forces / np.abs(tmpForces)
    return signs


def _setForceVectorLengthEle(boxes: list[EleLoadBox], vectScale=1):
    fscale0 = 0.4
    fstatic0 = 0.3

    forces = np.array([box.y for box in boxes])
    boxesOut = [None] * len(boxes)

    Fmax = np.max(np.abs(forces))

    # Get the sign of the maximum force. Ignores loads with sign changes
    signs = _getSigns(forces)

    # Find all force that are zero. These should remain zero
    Inds0 = np.where(np.abs(forces) == 0)

    # Plot the static portion, and the scale port of the force
    fscale = fscale0 * abs(forces) / Fmax
    fstatic = fstatic0 * np.ones_like(forces)
    fstatic[Inds0[0], Inds0[1]] = 0  # don't move the bottom of the plot!
    fplot = ((fscale + fstatic) * signs) * vectScale

    for ii in range(len(boxes)):
        boxOld = boxes[ii]

        dy = fplot[ii][1] - fplot[ii][0]
        # We scale fout appropriately and calcualte a new fint
        fout_fscale = fscale0 * (np.array(boxOld.fout) / Fmax)
        signs = _getSigns(fout_fscale)
        fout_plot = ((abs(fout_fscale) + fstatic0) * signs) * vectScale
        fint = (fout_plot - fplot[ii][0]) / dy
        boxesOut[ii] = EleLoadBox(boxOld.x, fplot[ii], list(fint))

    return boxesOut


def getInternalForces2D(node: Node2D, ind):
    """
    0 = axial force
    1 = shear force
    2 = moment
    """
    return node.Fint[[ind, ind + 3]]


@dataclass
class _NodeOutputs:
    xcoords: list[float]
    force: list[float]
    labels: list[str]



def plotVertDisp(beam: Beam, scale=1000, yunit='mm', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to
    plotting.

    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The scale to apply to y values of the plot. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.
    labelPlot : bool, optional
        Turns on or off the plot labels.

    Returns
    -------
    fig : matplotlib fig

    ax : matplotlib ax

    line : matplotlib line
        the plotted line.
    """

    return plotDisp(beam, 1, scale, yunit=yunit, **kwargs)


def plotRotation(beam: Beam, scale=1000, yunit='mRad', **kwargs):
    """
    Plots the rotation of a beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to
    plotting.

    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.
    labelPlot : bool, optional
        Turns on or off the plot labels.

    Returns
    -------
    fig : matplotlib fig

    ax : matplotlib ax

    line : matplotlib line
        the plotted line.
    """

    ind = beam.getDOF() - 1

    return plotDisp(beam, ind, scale, yunit=yunit, **kwargs)


def plotDisp(beam: Beam, index=1, scale=1000, xunit='m', yunit='mm',
             showAxis=True, showGrid=False, labelPlot=True,
             labelPOI=False, POIOptions=None):
    """
    Plots the displacement of one dimension of the beam. Each node will contain the
    relevant dispancement information. Analysis must be run on the beam prior to
    plotting.

    Parameters
    ----------
    beam : Beam
        The beam to plot internal forces with. The analysis must be run.
    index : int
        The type of response to plot, can have value 0:ux, 1: uy 2: rotation.
    scale : float, optional
        The scale to apply to y values of the plot. The default is 0.001.
    xunit : str, optional
        The xunit for the plot labels. The default is m.
    yunit : str, optional
        The yunit for the plot labels. The default is mm.
    showAxis : bool, optional
        Turns on or off the axis.
    showGrid : bool, optional
        Turns on or off the grid.
    labelPlot : bool, optional
        Turns on or off the plot labels.

    Returns
    -------
    fig : matplotlib fig

    ax : matplotlib ax

    line : matplotlib line
        the plotted line.

    """

    # Plotbeam....
    xcoords = np.zeros(beam.Nnodes)
    disp = np.zeros(beam.Nnodes)
    labels = [None] * beam.Nnodes

    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[index]
        labels[ii] = node.label

    fig, ax = _initOutputFig(showAxis, showGrid)
    _plotAxis(ax, xcoords, xunit, yunit, 'Displacement')
    disp = disp * scale

    if labelPlot:
        _plotLabels(ax, xcoords, disp, labels)

    line = plt.plot(xcoords, disp)

    if labelPOI:
        candidatePOI = findAllPOI(xcoords, disp, labels, POIOptions=POIOptions)
        filteredPoiInd = removeFalsePOI(candidatePOI, disp)
        plotPOI(fig, ax, xcoords, disp, labels, filteredPoiInd)

    return fig, ax, line