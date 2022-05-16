from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # To show dialog boxes for info/errors
from steel import steel_tables, historic_shapes  # Import DataFrames
from draw_W_section import draw_beam_section  # Import the beam drawing function


class SteelShapeSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steel Shape Selector")

        # Initialize variables
        self.use_historic = tk.BooleanVar(value=False)  # Historic Shape Checkbox Variable
        self.selected_shape = tk.StringVar()  # Shape selected by the user
        self.beam_length = tk.DoubleVar(value=20.0)  # Beam length (default 20 feet)

        # Checkbox to toggle between modern and historic shapes
        self.historic_checkbox = ttk.Checkbutton(
            root, text="Historic Shapes", variable=self.use_historic, command=self.update_shape_list
        )
        self.historic_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Label and autocomplete entry/dropdown
        self.search_label = ttk.Label(root, text="Search for a Shape:")
        self.search_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.search_entry = ttk.Entry(root, textvariable=self.selected_shape)
        self.search_entry.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.autocomplete)

        # Dropdown for autocomplete suggestions
        self.dropdown = tk.Listbox(root, height=5)
        self.dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.dropdown.bind("<<ListboxSelect>>", self.select_from_dropdown)

        # Frame to display selected shape properties
        self.properties_frame = ttk.Frame(root)
        self.properties_frame.grid(row=0, column=1, rowspan=6, padx=20, pady=10, sticky="n")

        self.property_labels = {}  # Store property labels dynamically

        # Add a button for drawing the section
        self.draw_button = ttk.Button(
            root, text="Draw Beam Section", command=self.draw_selected_section
        )
        self.draw_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Add a field for the beam length input (in feet)
        self.length_label = ttk.Label(root, text="Enter Beam Length (ft):")
        self.length_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.length_entry = ttk.Entry(root, textvariable=self.beam_length)
        self.length_entry.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        # Add a button to draw the beam with length
        self.length_draw_button = ttk.Button(
            root, text="Extrude Beam", command=self.extrude_beam
        )
        self.length_draw_button.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        # Load the initial shape list (modern shapes by default)
        self.update_shape_list()

    def update_shape_list(self):
        """
        Updates the list of shapes based on the selected data frame (modern or historic).
        """
        if self.use_historic.get():
            self.current_df = historic_shapes
            self.shape_column = "Name"
        else:
            self.current_df = steel_tables
            self.shape_column = "EDI_Std_Nomenclature"

        # Extract the list of shapes for the dropdown
        self.shapes = self.current_df[self.shape_column].dropna().unique().tolist()

        # Clear the dropdown list
        self.dropdown.delete(0, tk.END)

    def autocomplete(self, event):
        """
        Handles autocomplete functionality by filtering the list of shapes as the user types.
        """
        # Get current input
        user_input = self.search_entry.get().lower()

        # Filter shapes based on user input
        filtered_shapes = [shape for shape in self.shapes if user_input in shape.lower()]

        # Update the dropdown list
        self.dropdown.delete(0, tk.END)
        for shape in filtered_shapes:
            self.dropdown.insert(tk.END, shape)

    def select_from_dropdown(self, event):
        """
        Handles selection of a shape from the dropdown list and updates the text entry.
        Displays the properties of the selected shape.
        """
        # Get the selected item
        selected_index = self.dropdown.curselection()
        if selected_index:
            selected_shape = self.dropdown.get(selected_index)
            self.selected_shape.set(selected_shape)  # Update the text entry
            self.display_properties(selected_shape)  # Display properties

    def display_properties(self, shape_name):
        """
        Displays the properties of the selected steel shape in the properties_frame,
        using subscript codes for better formatting of the parameters.
        """
        # Clear existing property labels
        for label in self.property_labels.values():
            label.destroy()
        self.property_labels.clear()

        # Find the row corresponding to the selected shape
        shape_row = self.current_df[self.current_df[self.shape_column] == shape_name]
        if shape_row.empty:
            return  # If no matching shape is found, do nothing

        # Extract and format properties (add subscripts to keys for better display)
        properties = {
            "A": float(shape_row["A"].values[0]),
            "W": float(shape_row["W"].values[0]),
            "d (depth)": float(shape_row["d"].values[0]),
            "b\u2091 (flange width)": float(shape_row["bf"].values[0]),
            "t\u2091 (web thickness)": float(shape_row["tw"].values[0]),
            "t\u2091 (flange thickness)": float(shape_row["tf"].values[0]),
            "I\u2093 (Moment of inertia, x)": float(shape_row["Ix"].values[0]),
            "I\u2094 (Moment of inertia, y)": float(shape_row["Iy"].values[0]),
            "Z\u2093 (Section modulus, x)": float(shape_row["Zx"].values[0]),
            "Z\u2094 (Section modulus, y)": float(shape_row["Zy"].values[0]),
            "r\u2093 (Radius of gyration, x)": float(shape_row["rx"].values[0]),
            "r\u2094 (Radius of gyration, y)": float(shape_row["ry"].values[0]),
            "k\u2081 (Fillet Radius, k)": float(shape_row["k1"].values[0]),
        }

        # Display properties in the properties_frame
        row_index = 0
        for prop_name, prop_value in properties.items():
            label = ttk.Label(self.properties_frame, text=f"{prop_name}: {prop_value:.2f}")
            label.grid(row=row_index, column=0, sticky="w", pady=2)
            self.property_labels[prop_name] = label
            row_index += 1

        # Store the properties for drawing
        self.current_properties = properties

    def draw_selected_section(self):
        """
        Calls the draw_beam_section function with the selected shape's parameters.
        """
        if not hasattr(self, "current_properties") or not self.current_properties:
            messagebox.showerror("Error", "No shape selected or properties unavailable.")
            return

        try:
            # Extract relevant properties for drawing
            depth = self.current_properties["d (depth)"]
            flange_width = self.current_properties["bₑ (flange width)"]
            web_thickness = self.current_properties["tₑ (web thickness)"]
            flange_thickness = self.current_properties["tₑ (flange thickness)"]
            k = self.current_properties["k\u2081 (Fillet Radius, k)"]


            # Call the draw_beam_section function
            draw_beam_section(
                depth=depth / 12,
                flange_width=flange_width / 12,
                web_thickness=web_thickness / 12,
                flange_thickness=flange_thickness / 12,
                k=k / 12,
            )
            # messagebox.showinfo("Success", "Beam section drawn successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to draw the beam section: {e}")

    def extrude_beam(self):
        """
        Draws the beam with the specified length.
        """
        if not hasattr(self, "current_properties") or not self.current_properties:
            messagebox.showerror("Error", "No shape selected or properties unavailable.")
            return

        try:
            # Get the user-supplied length in feet
            length = self.beam_length.get()

            startPoint = DPoint3d(0.0, 0.0, 0.0)
            point = DPoint3d(0.0, 0.0, 0.0)

            startPoint.x = -0.27278702857479075750
            startPoint.y = -2.24278833315923531444
            startPoint.z = 2.29950808041501097989

            point.x = startPoint.x
            point.y = startPoint.y
            point.z = startPoint.z
            PyCadInputQueue.SendDataPoint(point, 1)
            PyCadInputQueue.SendKeyin("CHOOSE ALL ")
            PyCadInputQueue.SendKeyin("CONSTRUCT SURFACE PROJECTIONSOLID ")
            PyCExpression.SetCExpressionValue("tcb->ms3DToolSettings.extrude.solidIsDist", PyCExprValue(1),
                                              "SOLIDMODELING")
            PyCExpression.SetCExpressionValue("tcb->ms3DToolSettings.extrudeSolidDistance", PyCExprValue(
                ModelRef.GetUorPerMaster(ISessionMgr.ActiveDgnModelRef) * length), "SOLIDMODELING")

            point.x = startPoint.x + 0.27394178945524594315
            point.y = startPoint.y - 1.06879286342196166970
            point.z = startPoint.z + 0.79215858625165624929
            PyCadInputQueue.SendDataPoint(point, 1)

            point.x = startPoint.x + 1.24837185253013593922
            point.y = startPoint.y + 3.40942050240462446453
            point.z = startPoint.z + 0.79215858625165624929
            PyCadInputQueue.SendDataPoint(point, 1)

            PyCommandState.StartDefaultCommand()

            # Dummy operation as placeholder for provided code
            # messagebox.showinfo("Success", f"Beam of length {length:.2f} feet drawn successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not draw the beam: {e}")


# Create the Tkinter application
root = tk.Tk()
app = SteelShapeSelectorApp(root)
root.mainloop()
