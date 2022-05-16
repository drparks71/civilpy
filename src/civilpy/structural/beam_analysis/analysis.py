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
import numpy as np
from PyNite.FEModel3D import FEModel3D

from .baseclasses import Beam
from .loads import EleLoadDist, EleLoadLinear
from .output import OutputRecorderPyNite2D, OutputRecorder



try:
    import opensees as op
except:
    raise Exception(
        'OpenSeespy has not been installed. First include optional depependancy with "pip -m install planesections[opensees]"')


class PyNiteAnalyzer2D:

    def __init__(self, beam2D: Beam, recorder=OutputRecorderPyNite2D):

        self.beam: Beam = beam2D
        self._checkBeam(beam2D)

        self.Nnode = beam2D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = recorder

        self.nodeAnalysisNames = []
        self.memberNames = []

        self.matName = 'baseMat'

    def _checkBeam(self, beam2D):
        if not beam2D._dimension:
            raise Exception("The beam has no dimension, something terrible has happened.")
        if beam2D._dimension != '2D':
            raise Exception(f"The beam has dimension of type {beam2D._dimension}, it should have type '2D'")

    def initModel(self):


        self.analysisBeam = FEModel3D()

    def buildNodes(self):

        analysisBeam = self.analysisBeam

        for ii, node in enumerate(self.beam.nodes):
            name = 'N' + str(node.ID)
            self.nodeAnalysisNames.append(name)
            analysisBeam.add_node(name, node.x, 0, 0)

            if node.hasReaction:
                f1, f2, f3 = node.fixity.fixityValues
                analysisBeam.def_support(name, f1, f2, True, True, False, f3)

    def buildEulerBeams(self):

        beam = self.beam
        nodeAnalysisNames = self.nodeAnalysisNames
        E, G, A, Iz = beam.getMaterialPropreties()

        memberNames = []
        # this is sloppy, we supply empty values
        self.analysisBeam.add_material(self.matName, E, G, 0.3, 8000)
        for ii in range(self.Nele):
            memberName = 'M' + str(int(ii + 1))
            N1 = nodeAnalysisNames[ii]
            N2 = nodeAnalysisNames[ii + 1]
            self.analysisBeam.add_member(memberName, N1, N2, self.matName, 1., Iz, 1., A)
            memberNames.append(memberName)
        self.memberNames = memberNames

    def _buildPointLoads(self, pointLoads):
        for load in pointLoads:
            node = 'N' + str(load.nodeID)
            Fx, Fy, M = load.P
            self.analysisBeam.add_node_load(node, 'FY', Fy)
            self.analysisBeam.add_node_load(node, 'FX', Fx)
            self.analysisBeam.add_node_load(node, 'MZ', M)

    def buildPointLoads(self):

        self._buildPointLoads(self.beam.pointLoads)

    def analyze(self):

        self.analysisBeam.analyze(check_statics=False)

    def buildEleLoads(self):


        for eleload in self.beam.eleLoads:
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            build = self._selectLoad(eleload)
            build([N1, N2], eleload)

    def _selectLoad(self, eleload):
        if isinstance(eleload, EleLoadDist):
            return self._buildDistLoad
        if isinstance(eleload, EleLoadLinear):
            return self._buildLinLoad

    def _buildDistLoad(self, Nodes: list[int], eleload: EleLoadDist):
        N1, N2 = Nodes
        memberNames = self.memberNames
        q = eleload.P

        # We subtract one because node names are the index +1
        for ii in range(N1 - 1, N2 - 1):
            memberName = memberNames[ii]
            self.analysisBeam.add_member_dist_load(memberName, 'Fy', q[1], q[1])
            self.analysisBeam.add_member_dist_load(memberName, 'Fx', q[0], q[0])

    def _buildLinLoad(self, Nodes: list[int], eleload: EleLoadLinear):
        N1, N2 = Nodes
        memberNames = self.memberNames
        q = eleload.P
        for ii in range(N1 - 1, N2 - 1):  # shift one back because indicies are one less
            memberName = memberNames[ii]

            Node1 = self.beam.nodes[ii]
            Node2 = self.beam.nodes[ii + 1]

            qx1, qx2 = eleload.getLoadComponents(Node1.x, Node2.x, q[0])
            qy1, qy2 = eleload.getLoadComponents(Node1.x, Node2.x, q[1])

            self.analysisBeam.add_member_dist_load(memberName, 'Fy', qy1, qy2)
            self.analysisBeam.add_member_dist_load(memberName, 'Fx', qx1, qx2)

    def _getBeam(self):
        return self.analysisBeam

    def runAnalysis(self, recordOutput=True):


        self.initModel()
        self.buildNodes()
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()
        self.analyze()

        if recordOutput == True:
            self.recorder(self.beam, self.analysisBeam)


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


class OutputRecorderOpenSees(OutputRecorder):
    """
    An interface that can be used to get beam internal forces for each node
    in the model.
    When called on a beam, it will get all internal forces for that beam.
    Information at each node in the model is stored in the beam.
    The recorder is only is not instantiated at the time of recording.

    Parameters
    ----------
    beam : planesections Beam2D
        The beam whose data is being recorded.

    """

    def __init__(self, beam: Beam):

        self.Nnodes = beam.Nnodes
        self.nodeID0 = 1
        self.nodeIDEnd = self.Nnodes
        self.ndf = beam._ndf

        for ii, node in enumerate(beam.nodes):
            ID = node.ID
            node.disps = np.array(op.nodeDisp(ID))
            node.rFrc = np.array(op.nodeReaction(ID))
            node.Fint = self.getEleInteralForce(ID)

    def getEleInteralForce(self, nodID: int):
        """
        Gets the internal force at the left and right side of a node.
        The left and right side forces represent internal force at either side
        of a section cut.

        """
        ndf = self.ndf
        Fint = np.zeros(ndf * 2)
        if nodID == self.nodeID0:  # Left most node
            eleR = nodID
            # 0 is used to so that the plot "closes", i.e. starts at zero the goes up
            Fint[:ndf] = 0  # Left side forces
            Fint[ndf:] = op.eleForce(eleR)[:ndf]  # Right side forces

        # Direct Check, this is scary.
        elif nodID == self.nodeIDEnd:  # right side node
            eleL = nodID - 1
            Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:])  # Right side forces
            Fint[ndf:] = 0  # Left side forces
        else:  # center nodes
            eleL = nodID - 1
            eleR = nodID

            Fint[:ndf] = -np.array(op.eleForce(eleL)[ndf:])  # left entries
            Fint[ndf:] = np.array(op.eleForce(eleR)[:ndf])  # right entries

        return Fint


class OutputRecorder2D(OutputRecorderOpenSees):

    def __post_init__(self):
        raise Exception(
            'OutputRecorder2D is depcricated and will be removed in the next release. Use OutputRecorder instead')


class OpenSeesAnalyzer2D:
    """
    This class is used to  can be used to create and run an analysis of an
    input 2D beam using OpenSeesPy. The nodes, elements, sections, and
    forces for the beam are defined in the analysis model

    Note, nodes and elements will both start at 0 instead of 1.

    Parameters
    ----------
    beam : planesections Beam2D
        The beam whose data is being recorded.
    recorder : planesections Recorder
        The recorder to use for the output beam.
    geomTransform: str, optional
        The OpenSees Geometry transform to use. Can be "Linear" or "PDelta"
    clearOld : bool, optional
        A flag that can be used to turn on or off clearing the old analysis
        when the beam is created.
        There are some very niche cases where users may want to have mutiple
        beams at once in the OpenSees model.
        However, this should remain true for nearly all analyses.
        Do not turn on unless you know what you're doing.

    """

    def __init__(self, beam2D: Beam, recorder=OutputRecorderOpenSees,
                 geomTransform='Linear', clearOld=True):

        self.beam: Beam = beam2D
        self._checkBeam(beam2D)

        self.Nnode = beam2D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = recorder
        self.geomTransform = geomTransform
        self.clearOld = clearOld

    def _checkBeam(self, beam2D):
        if not beam2D._dimension:
            raise Exception("The beam has no dimension, something terible has happened.")
        if beam2D._dimension != '2D':
            raise Exception(f"The beam has dimension of type {beam2D._dimension}, it should have type '2D'")

    def initModel(self, clearOld=True):
        """
        Initializes the model.

        Parameters
        ----------
        clearOld : bool, optional
            A flag that can be used to turn on or off clearing the old analysis
            when the beam is created.
            There are some very niche cases where users may want to have mutiple
            beams at once in the OpenSees model.
            However, this should remain true for nearly all analyses.
            Do not turn on unless you know what you're doing.
        """

        if clearOld:
            op.wipe()
        op.model('Basic', '-ndm', 2)
        op.geomTransf(self.geomTransform, 1)

    def buildNodes(self):
        """
        Adds each node in the beam to the OpenSeesPy model, and assigns
        that node a fixity.
        """

        for node in self.beam.nodes:
            op.node(int(node.ID), float(node.x), 0.)

            # OpenSees is very finicky with these inputs, int them for saftey.
            f1, f2, f3 = node.fixity.fixityValues
            op.fix(node.ID, int(f1), int(f2), int(f3))

    def buildEulerBeams(self):
        """
        Creates an elastic Euler beam between each node in the model.
        """
        beam = self.beam
        E, G, A, Iz = beam.getMaterialPropreties()
        for ii in range(self.Nele):
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            # elasticBeamColumn eleTag iNode $jNode $A $E $Iz $transfTag <-release $relcode> <-mass $massDens> <-cMass>
            op.element(beam.EleType, eleID, Ni, Nj, A, E, Iz, 1)

    def _buildPointLoads(self, pointLoads):
        for load in pointLoads:
            op.load(int(load.nodeID), *load.P)

    def buildPointLoads(self):
        """
        Applies point loads to the appropriate nodes in the model.
        """
        op.timeSeries('Linear', 1)
        op.pattern('Plain', 1, 1)
        self._buildPointLoads(self.beam.pointLoads)

    def buildAnalysisPropreties(self):
        """
        Typical openSeesPy propreties that should work for any linear beam.
        A linear algorithm is used because there is no nonlienarity in the beam.
        """
        # op.constraints("Transformation")
        op.constraints("Lagrange")
        op.numberer("Plain")
        op.system('BandGeneral')
        op.test('NormDispIncr', 1. * 10 ** -8, 40, 0, 2)
        # op.algorithm('Newton')
        op.algorithm('Linear')
        op.integrator('LoadControl', 1.)
        op.analysis('Static')

    def analyze(self):
        """
        Analyzes the model once and records outputs.
        """
        ok = op.analyze(1)
        op.reactions()
        return ok

    def buildEleLoads(self):
        """
        Applies element loads to the appropriate elements in the model.
        """
        op.timeSeries('Linear', 2)
        op.pattern('Plain', 2, 2)

        for eleload in self.beam.eleLoads:
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            build = self._selectLoad(eleload)
            build([N1, N2], eleload)

    def _selectLoad(self, eleload):
        if isinstance(eleload, EleLoadDist):
            return self._buildDistLoad
        if isinstance(eleload, EleLoadLinear):
            return self._buildLinLoad

    def _buildDistLoad(self, Nodes: list[int], eleload: EleLoadLinear):
        load = eleload.P
        N1, N2 = Nodes[0], Nodes[1]
        for ii in range(N1, N2):
            op.eleLoad('-ele', int(ii),
                       '-type', '-beamUniform', load[1], load[0])

    def _buildLinLoad(self, Nodes: list[int], eleload: EleLoadLinear):
        load = eleload.P
        N1, N2 = Nodes[0], Nodes[1]
        for ii in range(N1, N2):
            Node1 = self.beam.nodes[ii - 1]
            Node2 = self.beam.nodes[ii]
            qx1, qx2 = eleload.getLoadComponents(Node1.x, Node2.x, load[0])
            qy1, qy2 = eleload.getLoadComponents(Node1.x, Node2.x, load[1])

            aOverL = 0.
            bOverL = 1.
            op.eleLoad('-ele', int(ii),
                       '-type', 'beamUniform',
                       qy1, qx1, aOverL, bOverL, qy2, qx2)

    def runAnalysis(self, recordOutput=True):
        """
        Makes and analyzes the beam in OpenSees.

        Returns
        -------
        None.

        """

        self.initModel(self.clearOld)
        self.buildNodes()
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()
        self.buildAnalysisPropreties()
        self.analyze()

        if recordOutput == True:
            self.recorder(self.beam)


class OpenSeesAnalyzer3D:
    """
    This class is used to  can be used to create and run an analysis of an
    input 2D beam using OpenSeesPy. The nodes, elements, sections, and
    forces for the beam are defined in the analysis model

    Note, nodes and elements will both start at 0 instead of 1.

    Parameters
    ----------
    beam : planesections Beam2D
        The beam whose data is being recorded.
    recorder : planesections Recorder
        The recorder to use for the output beam.
    geomTransform: str, optional
        The OpenSees Geometry transform to use. Can be "Linear" or "PDelta"
    clearOld : bool, optional
        A flag that can be used to turn on or off clearing the old analysis
        when the beam is created.
        There are some very niche cases where users may want to have mutiple
        beams at once in the OpenSees model.
        However, this should remain true for nearly all analyses.
        Do not turn on unless you know what you're doing.

    """

    def __init__(self, beam3D: Beam, recorder=OutputRecorderOpenSees,
                 geomTransform='Linear', clearOld=True):

        self.beam = beam3D
        self._checkBeam(beam3D)

        self.Nnode = beam3D.Nnodes
        self.Nele = self.Nnode - 1
        self.recorder = OutputRecorderOpenSees
        self.geomTransform = geomTransform
        self.clearOld = clearOld

    def _checkBeam(self, beam3D):
        if not beam3D._dimension:
            raise Exception("The beam has no dimension, something terible has happened.")
        if beam3D._dimension != '3D':
            raise Exception(f"The beam has dimension of type {beam3D._dimension}, it should have type '3D'")

    def initModel(self, clearOld=True):
        """
        Initializes the model.

        Parameters
        ----------
        clearOld : bool, optional
            A flag that can be used to turn on or off clearing the old analysis
            when the beam is created.
            There are some very niche cases where users may want to have mutiple
            beams at once in the OpenSees model.
            However, this should remain true for nearly all analyses.
            Do not turn on unless you know what you're doing.
        """

        if clearOld:
            op.wipe()
        op.model('Basic', '-ndm', 3)
        # see https://opensees.berkeley.edu/wiki/index.php/PDelta_Transformation
        op.geomTransf(self.geomTransform, 1, *[0, 0, 1])

    def buildNodes(self):
        """
        Adds each node in the beam to the OpenSeesPy model, and assigns
        that node a fixity.
        """

        for node in self.beam.nodes:
            op.node(int(node.ID), float(node.x), 0., 0.)

            # OpenSees is very finicky with these inputs, int them for saftey.
            f1, f2, f3, f4, f5, f6 = node.fixity.fixityValues
            op.fix(node.ID, int(f1), int(f2), int(f3), int(f4), int(f5), int(f6))

    def buildEulerBeams(self):
        """
        Creates an elastic Euler beam between each node in the model.
        """
        beam = self.beam
        E, G, A, Iz, Iy, J = beam.getMaterialPropreties()
        for ii in range(self.Nele):
            ID = ii + 1
            eleID = int(ID)
            Ni = int(ID)
            Nj = int(ID + 1)
            # element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)
            op.element(beam.EleType, eleID, Ni, Nj, A, E, G, J, Iy, Iz, 1)

    def buildPointLoads(self):
        """
        Applies point loads to the appropriate nodes in the model.
        """
        op.timeSeries('Linear', 1)
        op.pattern('Plain', 1, 1)
        for load in self.beam.pointLoads:
            op.load(int(load.nodeID), *load.P)

    def buildAnalysisPropreties(self):
        """
        Typical openSeesPy propreties that should work for any linear beam.
        A linear algorithm is used because there is no nonlienarity in the beam.
        """
        # op.constraints("Transformation")
        op.constraints("Lagrange")
        op.numberer("Plain")
        op.system('BandGeneral')
        op.test('NormDispIncr', 1. * 10 ** -8, 40, 0, 2)
        # op.algorithm('Newton')
        op.algorithm('Linear')
        op.integrator('LoadControl', 1.)
        op.analysis('Static')

    def analyze(self):
        """
        Analyzes the model once and records outputs.
        """
        ok = op.analyze(1)
        op.reactions()

    def buildEleLoads(self):
        """
        Applies element loads to the appropriate elements in the model.
        """
        op.timeSeries('Linear', 2)
        op.pattern('Plain', 2, 2)

        for eleload in self.beam.eleLoads:
            N1 = self.beam._findNode(eleload.x1) + 1
            N2 = self.beam._findNode(eleload.x2) + 1
            load = eleload.P

            for ii in range(N1, N2):
                # eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint',Py,<Pz>,xL,Px=0.0,'-beamThermal',*tempPts)
                op.eleLoad('-ele', int(ii), '-type', '-beamUniform', load[1], load[2], load[0])

    def runAnalysis(self, recordOutput=True):
        """
        Makes and analyzes the beam in OpenSees.

        Returns
        -------
        None.

        """

        self.initModel(self.clearOld)
        self.buildNodes()
        self.buildEulerBeams()
        self.buildPointLoads()
        self.buildEleLoads()
        self.buildAnalysisPropreties()
        self.analyze()

        if recordOutput == True:
            self.recorder(self.beam)


def getDisp(beam: Beam, ind: int):
    """
    Gets the beam displacement along the axis specified for the index.

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get
        data.
    ind : int
        The index of the axis to read from. Can have value 0: horizontal
        displacement
        1: vertical displacement
        2: rotation.

    Returns
    -------
    disp : numpy array
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """

    xcoords = np.zeros(beam.Nnodes)
    disp = np.zeros(beam.Nnodes)
    for ii, node in enumerate(beam.nodes):
        xcoords[ii] = node.x
        disp[ii] = node.disps[ind]
    return disp, xcoords


def getVertDisp(beam: Beam):
    """
    Gets the beam vertical displacement for the beam

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get
        data.

    Returns
    -------
    disp : numpy array
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """
    return getDisp(beam, 1)


def getMaxVertDisp(beam: Beam):
    """
    Gets the absolute value of beam vertical displacement and it's location.

    Parameters
    ----------
    beam : Beam
        The beam to read displacement from. The beam must be analyzed to get
        data.

    Returns
    -------
    dispMax : float
        The displacement at each x coordinant.
    xcoords : numpy array
        The x coordinants.
    """
    disp, x = getVertDisp(beam)
    dispAbs = np.abs(disp)
    ind = np.argmax(dispAbs)
    return disp[ind], x[ind]


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