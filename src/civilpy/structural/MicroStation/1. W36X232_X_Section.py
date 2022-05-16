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