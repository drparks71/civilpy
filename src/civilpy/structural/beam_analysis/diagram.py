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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from .loads import PointLoadOptions, DistLoadOptions, LinLoadOptions, MomentPointLoadOptions



class AbstractDiagramElement(ABC):
    @abstractmethod
    def plot(self):
        pass


class DiagramEleLabel:
    def __init__(self, xy0, label, labelOptions):
        self.xy0 = xy0
        self.label = label
        self.labelOffset = labelOptions.labelOffset
        self.textKwargs = labelOptions.textKwargs

    def plot(self, ax):
        x = self.xy0[0] + self.labelOffset
        y = self.xy0[1] + self.labelOffset
        ax.text(x, y, self.label, self.textKwargs)


class DiagramElePointLoad(AbstractDiagramElement):
    def __init__(self, xy0, dxy0, options: PointLoadOptions):
        self.xy0 = xy0
        self.dxy0 = dxy0
        self.width = options.lw
        self.arrowWidth = options.arrowWidth
        self.c = options.c

    def plot(self, ax):

        x, y = self.xy0
        Px, Py = self.dxy0
        c = self.c

        width = self.width
        hwidth = self.arrowWidth
        length = self.arrowWidth
        ax.arrow(x, y, Px, Py, width=width, head_width=hwidth,
                 head_length=length, edgecolor='none',
                 length_includes_head=True, fc=c)


class DiagramEleLoadDistributed(AbstractDiagramElement):
    def __init__(self, loadBox, diagramOptions: DistLoadOptions,
                 plOptions: PointLoadOptions):
        self.loadBox = loadBox
        # self.pointUp = loadBox.pointUp
        self.options = diagramOptions
        self.plOptions = plOptions
        self.minNbar = 3

    def plot(self, ax):

        barWidth = self.options.barWidth
        spacing = self.options.spacing
        barC = self.options.c
        x1, x2 = self.loadBox.x
        y1, y2 = self.loadBox.y

        N = max(int((x2 - x1) / spacing) + 1, self.minNbar)
        xVals = np.linspace(x1, x2, N)

        ystart = self.loadBox.fout[0]
        yend = self.loadBox.datum
        dy = ystart - yend

        xbar = [x1, x2]
        yBarS = [ystart, ystart]
        yBarE = [yend, yend]
        plt.plot(xbar, yBarS, linewidth=barWidth, c=barC)
        plt.plot(xbar, yBarE, linewidth=barWidth, c=barC)

        for ii in range(N):
            x = xVals[ii]
            # pointLoad = DiagramElePointLoad((x, ystart), (0, yend), self.plOptions)
            pointLoad = DiagramElePointLoad((x, ystart), (0, -dy), self.plOptions)
            pointLoad.plot(ax)


class DiagramEleLoadLinear(AbstractDiagramElement):

    def __init__(self, loadBox, diagramOptions: LinLoadOptions,
                 plOptions: PointLoadOptions):
        self.loadBox = loadBox
        self.options = diagramOptions
        self.plOptions = plOptions
        self.minNbar = 3

    def plot(self, ax):


        barWidth = self.options.barWidth
        minLengthCutoff = self.options.minLengthCutoff
        spacing = self.options.spacing
        barC = self.options.c
        x1, x2 = self.loadBox.x
        # y1, y2 = self.loadBox.y

        # baseLineWidth = 0.015

        Nlines = max(int((x2 - x1) / spacing) + 1, self.minNbar)

        xVals = np.linspace(x1, x2, Nlines)

        q1, q2 = self.loadBox.fout
        yVals = np.linspace(q1, q2, Nlines)

        # The top/bottom lines .
        ydatum = self.loadBox.datum
        xbar = [x1, x2]
        yBardatum = [ydatum, ydatum]
        yBarLinear = [q1, q2]

        plt.plot(xbar, yBardatum, linewidth=barWidth, c=barC)
        plt.plot(xbar, yBarLinear, linewidth=barWidth, c=barC)

        for ii in range(Nlines):
            xline = xVals[ii]
            yLine = yVals[ii]

            # plot just the line with no arrow
            if abs(yLine - ydatum) > minLengthCutoff:
                xy0 = (xline, yLine)
                dxy0 = (0, ydatum - yLine)
                load = DiagramElePointLoad(xy0, dxy0, self.plOptions)
                load.plot(ax)

            # plot line and arrow.
            else:
                width = self.plOptions.lw
                ax.plot([xline, xline], [yLine, ydatum], c=barC,
                        linewidth=barWidth * 0.5)


class DiagramEleMoment(AbstractDiagramElement):

    def __init__(self, xy0, diagramOptions: MomentPointLoadOptions,
                 isPositive=False):
        self.xy0 = xy0
        self.options = diagramOptions
        self.c = diagramOptions.c
        self.r = diagramOptions.r

        self.rotationAngle = diagramOptions.rotationAngle

        self.isPositive = isPositive

    def _getFixedSupportCords(self, positive):


        r = self.r
        arrow = r / 4
        arclength = 1 * 2 * np.pi

        # Get base rectangle point.
        t = np.linspace(0.0, 0.8, 31) * arclength
        x = r * np.cos(t)
        y = r * np.sin(t)

        if positive:
            ind = -1
            x0c = x[ind]
            y0c = y[ind]
            xarrow = [x0c - arrow * 1.2, x0c, x0c - arrow * 1.2]
            yarrow = [y0c + arrow * 1.5, y0c, y0c - arrow * 1.5]

        if not positive:
            ind = 0
            x0c = x[ind]
            y0c = y[ind]
            xarrow = [x0c - arrow * 1.5, x0c, x0c + arrow * 1.5]
            yarrow = [y0c + arrow * 1.2, y0c, y0c + arrow * 1.2]

        return x, y, xarrow, yarrow

    def plot(self, ax):

        lw = self.options.lw
        x, y, xarrow, yarrow = self._getFixedSupportCords(self.isPositive)
        rInner = self.r / 5

        # Define a rotation matrix
        theta = np.radians(self.rotationAngle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))

        # rotate the vectors
        xy = np.column_stack([x, y])
        xyArrow = np.column_stack([xarrow, yarrow])
        xyOut = np.dot(xy, R.T)
        xyArrowOut = np.dot(xyArrow, R.T)

        # Shift to the correct location

        x0 = self.xy0[0]
        xyOut[:, 0] += x0
        xyArrowOut[:, 0] += x0
        xy0 = [x0, 0]

        c = self.options.c
        ax.add_patch(Circle(xy0, rInner, facecolor=c, fill=True, zorder=2, lw=lw))

        plt.plot(xyOut[:, 0], xyOut[:, 1])
        plt.plot(xyArrowOut[:, 0], xyArrowOut[:, 1], c=c)