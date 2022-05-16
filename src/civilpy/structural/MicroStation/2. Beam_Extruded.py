from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)


startPoint.x = -0.27278702857479075750
startPoint.y = -2.24278833315923531444
startPoint.z = 2.29950808041501097989

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)
PyCadInputQueue.SendKeyin ("CONSTRUCT SURFACE PROJECTIONSOLID " )
PyCExpression.SetCExpressionValue ("tcb->ms3DToolSettings.extrude.solidIsDist", PyCExprValue(1), "SOLIDMODELING")
PyCExpression.SetCExpressionValue ("tcb->ms3DToolSettings.extrudeSolidDistance", PyCExprValue (ModelRef.GetUorPerMaster (ISessionMgr.ActiveDgnModelRef) * 20), "SOLIDMODELING")

point.x = startPoint.x + 0.27394178945524594315
point.y = startPoint.y - 1.06879286342196166970
point.z = startPoint.z + 0.79215858625165624929
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 1.24837185253013593922
point.y = startPoint.y + 3.40942050240462446453
point.z = startPoint.z + 0.79215858625165624929
PyCadInputQueue.SendDataPoint (point, 1)

PyCommandState.StartDefaultCommand()