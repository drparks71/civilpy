from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *


def draw_beam_section(depth, flange_width, web_thickness, flange_thickness, k):
    """
    Draw the cross-section of a beam based on its dimensions.

    :param depth: Total vertical depth of the beam.
    :param flange_width: Width of the flange (both top and bottom).
    :param web_thickness: Thickness of the web.
    :param flange_thickness: Thickness of both top and bottom flanges.
    :param k: K_det value for the fillets.
    """
    # Activate the appropriate level to draw
    PyCadInputQueue.SendKeyin("ACTIVE LEVEL \"Structure\"")
    PyCadInputQueue.SendKeyin("PLACE SMARTLINE")

    # Intermediate calculations for offsets
    top_flange_width = (flange_width - web_thickness) / 2
    web_height = depth - (2 * flange_thickness)

    # Points for the cross-section (x and z offsets are calculated based on dimensions)
    points = [
        (0, 0),  # Point 0: Bottom Left Flange Bottom
        (flange_width, 0),  # Point 1: Bottom Right Flange Bottom
        (flange_width, flange_thickness),  # Point 2: Bottom Right Flange Top
        (flange_width - (top_flange_width - k), flange_thickness),  # Point 3: Bottom Flange Right Web
        (flange_width - (top_flange_width - k), flange_thickness + k),  # Point 4: Fillet midpoint
        (flange_width - top_flange_width, flange_thickness + k),  # Point 5: Fillet End
        (flange_width - top_flange_width, flange_thickness + web_height - k),  # Point 6: Top Right fillet start
        (flange_width - top_flange_width + k, flange_thickness + web_height - k),  # Point 7: Top Right Fillet Center
        (flange_width - top_flange_width + k, flange_thickness + web_height),  # Point 8: Top Right Fillet end
        (flange_width, flange_thickness + web_height),  # Point 9: Top Flange Right Bottom
        (flange_width, depth),  # Point 10: Top flange top right
        (0, depth),  # Point 11: Top flange top left
        (0, depth - flange_thickness),  # Point 12: Top flange bottom left
        (top_flange_width - k, depth - flange_thickness),  # Point 13: Top left fillet start
        (top_flange_width - k, depth - (flange_thickness+k)),  # Point 14: Top left fillet center
        (top_flange_width, depth - (flange_thickness+k)),  # Point 15: Top left fillet end
        (top_flange_width, flange_thickness + k),  # Point 16: Bottom left fillet start
        (top_flange_width - k, flange_thickness + k),  # Point 17: Bottom left fillet center
        (top_flange_width - k, flange_thickness),  # Point 18: Bottom left fillet end
        (0, flange_thickness),  # Point 19: Bottom Flange Left Top
        (0, 0)  # Point 20: Origin
    ]

    # Send all points to Bentley API
    for index, point in enumerate(points):
        if index in [3, 6, 13, 16]:
            PyCadInputQueue.SendDataPoint(DPoint3d(point[0], 0, point[1]), 1)
            PyCadInputQueue.SendKeyin("SMARTLINE SEGMENT ARCS ")

        elif index in [4, 7, 14, 17]:
            PyCadInputQueue.SendDataPoint(DPoint3d(point[0], 0, point[1]), 1)
            PyCExpression.SetCExpressionValue("smrtlineInfo.cwArcs", PyCExprValue(1), "SMRTLINE")
            PyCExpression.SetCExpressionValue("smrtlineInfo.bigArc", PyCExprValue(0), "SMRTLINE")

        elif index in [5, 8, 15, 18]:
            PyCadInputQueue.SendDataPoint(DPoint3d(point[0], 0, point[1]), 1)
            PyCadInputQueue.SendKeyin("SMARTLINE SEGMENT LINES ")

        else:
            PyCadInputQueue.SendDataPoint(DPoint3d(point[0], 0, point[1]), 1)

    # Finalize the drawing
    PyCadInputQueue.SendReset()
    PyCommandState.StartDefaultCommand()


# Example Usage:
# Draw a W36X232 beam cross-section (dimensions converted to feet)
draw_beam_section(
    depth=37.1 / 12,
    flange_width=12.1 / 12,
    web_thickness=0.87 / 12,
    flange_thickness=1.57 / 12,
    k = 1.625 / 12
)
