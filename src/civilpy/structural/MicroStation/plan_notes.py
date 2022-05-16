from MSPyBentley import *
from MSPyBentleyGeom import *
from MSPyECObjects import *
from MSPyDgnPlatform import *
from MSPyMstnPlatform import *

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

from pathlib import Path


class PlanNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plan Notes")

        # Load notes from JSON file
        self.notes_data = self.load_notes()

        # Create a frame for categories
        self.category_frame = ttk.Frame(self.root)
        self.category_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Create a frame for notes
        self.notes_frame = ttk.Frame(self.root)
        self.notes_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsw")

        # Category Label and List
        self.category_label = ttk.Label(self.category_frame, text="Categories:")
        self.category_label.pack(anchor="w", padx=5, pady=5)

        self.category_listbox = tk.Listbox(self.category_frame, height=15, width=25)
        self.category_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        self.category_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        # Populate categories
        self.populate_categories()

        # Notes Label and List
        self.notes_label = ttk.Label(self.notes_frame, text="Plan Notes:")
        self.notes_label.pack(anchor="w", padx=5, pady=5)

        self.notes_listbox = tk.Listbox(self.notes_frame, height=15, width=50)
        self.notes_listbox.pack(padx=5, pady=5, fill="both", expand=True)

        # Place Note Button
        self.note_counter = 0
        self.place_note_button = ttk.Button(self.notes_frame, text="Place Note", command=self.place_note)
        self.place_note_button.pack(pady=10)

    def load_notes(self):
        """
        Load the plan notes from the JSON file.
        """
        try:
            macros_folder = Path(os.getcwd()).parent.parent / 'Standards/Macros/Plan Notes Tool/res/plan_notes.json'
            json_file_path = macros_folder
            with open(json_file_path, "r") as file:
                notes_data = json.load(file)
            return notes_data
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find 'plan_notes.json' in the 'res' folder.")
            self.root.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in 'plan_notes.json'.")
            self.root.destroy()
        return {}

    def populate_categories(self):
        """
        Populate the category Listbox with categories from plan_notes.json.
        """
        for category in self.notes_data:
            self.category_listbox.insert(tk.END, category)

    def on_category_select(self, event):
        """
        Populate the notes Listbox when a category is selected.
        """
        selected_category = self.category_listbox.curselection()
        if not selected_category:
            return

        category_name = self.category_listbox.get(selected_category)
        self.notes_listbox.delete(0, tk.END)

        # For each note (list of strings), join strings with '\n' and insert into the Listbox
        for note_list in self.notes_data.get(category_name, []):
            note_content = "\n".join(note_list)  # Join list of strings with '\n'
            self.notes_listbox.insert(tk.END, note_content)

    def place_note(self):
        """
            Copy selected note to clipboard and exit the application.
            """
        selected_note_idx = self.notes_listbox.curselection()
        if not selected_note_idx:
            messagebox.showwarning("Warning", "Please select a note to place.")
            return

        # Get the content of the selected note
        note_content = self.notes_listbox.get(selected_note_idx)

        # Copy note content to the clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(note_content)
        self.root.update()  # Keep the clipboard content after program exit

        # Send commands to MicroStation
        PyCadInputQueue.SendKeyin("TEXTEDITOR PLACE ")
        PyCadInputQueue.SendKeyin(f"TEXTEDITOR PLAYCOMMAND INSERT_TEXT \"{self.note_counter + 1}. \"")
        PyCadInputQueue.SendCommand("TEXTEDITOR PLAYCOMMAND PASTE")

        self.note_counter += 1

        # Exit the application
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlanNotesApp(root)
    root.mainloop()
