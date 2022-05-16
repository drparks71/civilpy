from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)

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
