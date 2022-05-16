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

from .baseclasses import Beam


class OutputRecorder(ABC):
    Nnodes: int
    nodeID0: float
    nodeIDEnd: int
    ndf: int
    node: list

    @abstractmethod
    def getEleInteralForce(self):
        pass


class OutputRecorderPyNite2D(OutputRecorder):
    lcName = 'Combo 1'

    def __init__(self, beam: Beam, analysisBeam):
        self.Nnodes = beam.Nnodes
        self.nodeID0 = 1
        self.nodeIDEnd = self.Nnodes
        self.ndf = beam._ndf
        self.analysisBeam = analysisBeam
        for ii, ID in enumerate(analysisBeam.nodes.keys()):
            analysisNode = analysisBeam.nodes[ID]
            disps = [analysisNode.DX[self.lcName], analysisNode.DY[self.lcName], analysisNode.RZ[self.lcName]]
            rFrc = [analysisNode.RxnFX[self.lcName], analysisNode.RxnFY[self.lcName], analysisNode.RxnMZ[self.lcName]]

            # assign values
            node = beam.nodes[ii]
            node.disps = np.array(disps)
            node.rFrc = np.array(rFrc)
            node.Fint = self.getEleInteralForce(ii)

    def _getFint(self, ele):
        PyL, PyR = ele.axial_array(2)[1]
        VyL, VyR = ele.shear_array('Fy', 2)[1]
        MyL, MyR = ele.moment_array('Mz', 2)[1]

        return np.array([PyL, VyL, MyL]), np.array([PyR, VyR, MyR])

    def getEleInteralForce(self, nodeID: int):

        ndf = self.ndf
        Fint = np.zeros(ndf * 2)

        nodeID += 1

        if nodeID == self.nodeID0:  # Left most node
            eleRID = 'M' + str(nodeID)
            eleR = self.analysisBeam.members[eleRID]
            # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
            Fint[:ndf] = 0

            FeleR_L, _ = self._getFint(eleR)
            Fint[ndf:] = FeleR_L  # Left side forces for right side element

        elif nodeID == self.nodeIDEnd:  # right side node
            eleLID = 'M' + str(int(nodeID - 1))
            eleL = self.analysisBeam.members[eleLID]

            _, FeleL_R = self._getFint(eleL)
            Fint[:ndf] = FeleL_R  # Right side forces
            Fint[ndf:] = 0
            # Left side forces
        else:  # center nodes

            eleLID = 'M' + str(int(nodeID - 1))
            eleRID = 'M' + str(int(nodeID))
            eleL = self.analysisBeam.members[eleLID]
            eleR = self.analysisBeam.members[eleRID]
            _, FeleL_R = self._getFint(eleL)
            FeleR_L, _ = self._getFint(eleR)

            Fint[:ndf] = FeleL_R  # left entries
            Fint[ndf:] = FeleR_L  # right entries

        return Fint