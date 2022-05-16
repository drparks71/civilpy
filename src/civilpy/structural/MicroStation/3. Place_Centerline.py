from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

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