from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *
import tkinter as tk
from tkinter import messagebox


# Function to copy beams with user-specified spacing
def copy_beams_with_spacing(spacing):
    try:
        spacing_ft = float(spacing)  # Convert user input to a float representing feet

        startPoint = DPoint3d(0.0, 0.0, 0.0)
        point = DPoint3d(0.0, 0.0, 0.0)

        # Coordinates of the original beam position
        startPoint.x = 10.19653965669150963436
        startPoint.y = 3.95163276186758283259
        startPoint.z = 1.85450734129565608654

        point.x = startPoint.x
        point.y = startPoint.y
        point.z = startPoint.z
        PyCadInputQueue.SendDataPoint(point, 1)
        PyCadInputQueue.SendKeyin("CHOOSE ALL")
        PyCadInputQueue.SendKeyin("COPY ICON")

        # Perform 3 copies (add 3 beams for a total of 4 beams including the original one)
        for i in range(1, 5):  # Loop starts from 1 and ends at 3 (3 copies)
            point.x = startPoint.x + i * spacing_ft  # Calculate new X positions based on spacing
            point.y = startPoint.y  # Y and Z remain constant
            point.z = startPoint.z
            PyCadInputQueue.SendDataPoint(point, 1)

        # Reset and return to default state
        PyCadInputQueue.SendReset()
        PyCommandState.StartDefaultCommand()

        messagebox.showinfo("Success", f"Beams copied 3 times (total 4 beams) with spacing: {spacing_ft}'")
    except ValueError:
        # Handle invalid input gracefully
        messagebox.showerror("Error", "Invalid spacing value. Please enter a numeric value.")


# Function to handle Tkinter button click
def handle_submit():
    spacing = spacing_entry.get()
    copy_beams_with_spacing(spacing)


# Setting up Tkinter GUI
root = tk.Tk()
root.title("Beam Spacing Input")

tk.Label(root, text="Enter beam spacing (in feet):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
spacing_entry = tk.Entry(root)
spacing_entry.grid(row=0, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Submit", command=handle_submit)
submit_button.grid(row=1, columnspan=2, pady=10)

root.mainloop()
