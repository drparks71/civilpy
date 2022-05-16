from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

startPoint = DPoint3d (0.0, 0.0, 0.0)
point      = DPoint3d (0.0, 0.0, 0.0)

PyCadInputQueue.SendKeyin ("PLACE LINE CONSTRAINED " )

startPoint.x = 2078423.77082349266856908798
startPoint.y = 624143.77882429817691445351
startPoint.z = 0.00000000000000000000

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 14.50000000000000000000
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 14.50000000000000000000
point.y = startPoint.y - 2.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 8.25000000000000000000
point.y = startPoint.y - 2.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 8.25000000000000000000
point.y = startPoint.y - 14.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 14.50000000000000000000
point.y = startPoint.y - 14.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 14.50000000000000000000
point.y = startPoint.y - 16.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y - 16.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y - 14.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 6.25000000000000000000
point.y = startPoint.y - 14.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 6.25000000000000000000
point.y = startPoint.y - 2.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y - 2.00000000000000000000
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

point.x = startPoint.x + 14.50000000000000000000
point.y = startPoint.y
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

PyCadInputQueue.SendReset()
PyCadInputQueue.SendKeyin ("INPUTMANAGER TRAINING HINT " )
PyCadInputQueue.SendKeyin ("CHOOSE ELEMENT " )

point.x = startPoint.x - 1.38836251967586576939
point.y = startPoint.y + 19.41612487437669187784
point.z = startPoint.z
PyCadInputQueue.SendDataPoint (point, 1)

PyCommandState.StartDefaultCommand()