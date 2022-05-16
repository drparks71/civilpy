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

the beam_analysis library based originally off of planesections available at:
https://github.com/cslotboom/planesections (Apache 2.0)
"""
from .baseclasses import (Section, SectionBasic, SectionRectangle, Node2D, Node3D, Beam, newEulerBeam,
                          newSimpleEulerBeam, EulerBeam, EleLoadDist, EleLoadLinear, PointLoad, FixityTypes2D
                          )
from .loads import PointLoad, EleLoadLinear
from .supports import FixityTypes2D, NAMED_RELEASES_2D
from .analysis import (PyNiteAnalyzer2D)
try:
    from .analysis import (OutputRecorder2D, OutputRecorder,
                           OpenSeesAnalyzer2D, OpenSeesAnalyzer3D)
except:
    pass

from .analysis import (getDisp, getVertDisp, getMaxVertDisp)
from .plot_functions import (plotInternalForce, plotShear, plotMoment, plotBeamDiagram, BeamPlotter2D,
                       plotDisp, plotVertDisp, plotRotation,
                       getInternalForces2D)

from .configure import DiagramUnitEnvironmentHandler
diagramUnits = DiagramUnitEnvironmentHandler()

