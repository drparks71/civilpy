from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)

PyCadInputQueue.SendKeyin ("ACTIVE LEVEL \"Structure\"" )
PyCadInputQueue.SendKeyin ("PLACE SMARTLINE " )

startPoint.x = -0.50301190578621146621
startPoint.y = -3.31158119658119698414
startPoint.z = 3.09166666666666722918

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 1.00833333333333330373
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 1.00833333333333330373
point.y = startPoint.y
point.z = startPoint.z - 0.13083333333333380111
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.54041666666666721142
point.y = startPoint.y
point.z = startPoint.z - 0.13083333333333380111
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.54041666666666676733
point.y = startPoint.y
point.z = startPoint.z - 2.96083333333333298398
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 1.00833333333333352577
point.y = startPoint.y
point.z = startPoint.z - 2.96083333333333342807
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 1.00833333333333330373
point.y = startPoint.y
point.z = startPoint.z - 3.09166666666666722918
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.00000000000000022204
point.y = startPoint.y
point.z = startPoint.z - 3.09166666666666722918
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.00000000000000033307
point.y = startPoint.y
point.z = startPoint.z - 2.96083333333333342807
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.46791666666666686947
point.y = startPoint.y
point.z = startPoint.z - 2.96083333333333431625
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.46791666666666686947
point.y = startPoint.y
point.z = startPoint.z - 0.13083333333333424520
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.00000000000000011102
point.y = startPoint.y
point.z = startPoint.z - 0.13083333333333380111
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

PyCadInputQueue.SendReset()

PyCommandState.StartDefaultCommand()

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


startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)

PyCadInputQueue.SendKeyin ("ACTIVE LEVEL \"StructuralCourse\"" )
PyCadInputQueue.SendKeyin ("PLACE SMARTLINE " )

startPoint.x = 0.00115476088045516007
startPoint.y = -3.31158119658119698414
startPoint.z = 3.09166666666666722918

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y + 20.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

PyCadInputQueue.SendReset()

PyCommandState.StartDefaultCommand()

startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)


startPoint.x = 11.90242123910005389575
startPoint.y = -5.40294846655439453542
startPoint.z = -0.58511042756472309012

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)
PyCadInputQueue.SendKeyin ("CHOOSE ALL " )
PyCadInputQueue.SendKeyin ("COPY ICON " )

point.x = startPoint.x - 11.39709981155293228028
point.y = startPoint.y + 2.09136726997320199217
point.z = startPoint.z + 0.58511042756472342319
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 0.60290018844706949608
point.y = startPoint.y + 2.09136726997320199217
point.z = startPoint.z + 0.58511042756472309012
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 12.60290018844706949608
point.y = startPoint.y + 2.09136726997320199217
point.z = startPoint.z + 0.58511042756472309012
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 24.60290018844706949608
point.y = startPoint.y + 2.09136726997320199217
point.z = startPoint.z + 0.58511042756472309012
PyCadInputQueue.SendDataPoint (point, 1)

PyCadInputQueue.SendReset()

PyCommandState.StartDefaultCommand()
