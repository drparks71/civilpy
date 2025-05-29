import os
import json
from pathlib import Path
import ipywidgets as widgets
from datetime import datetime, date
from IPython.display import display
from .stage_2_comments import all_criteria


class Stage2StructuralChecklist:
    """
    Manages and organizes the creation of a structural checklist for Stage 2 projects.

    This class provides mechanisms to initialize, configure, and update project-specific
    checklists, allowing users to input project details, submit them through interactive
    widgets in Jupyter Lab, and manage project review data effectively.
    """
    def __init__(self, pid=''):
        # Initialize to store widgets and data
        check_if_review_folder_exists()

        self.data = {'Scope': {}}
        if pid:
            self.data['Project Info'] = {'pid': pid}
            self.inputs = {}
            self.define_project_inputs()
            self.inputs['pid'].value = pid
            try:
                self.load_project_info(None)
            except Exception as e:
                print(f'Project data for pid {pid} not found: {e}')
        else:
            self.data['Project Info'] = {}
            self.inputs = {}
            self.define_project_inputs()

    def define_project_inputs(self):
        """Create input fields for project info and a submit button."""
        try:
            if self.data['Project Info']['pid']:
                # Define input widgets - Previous Data
                self.inputs['cty_rte_sec'] = widgets.Text(
                    description='CTY-RTE-SEC: ',
                    value=self.data['Project Info']['cty_rte_sec']
                )
                self.inputs['checker'] = widgets.Text(
                    description='Checked By: ',
                    value=self.data['Project Info']['checker']
                )
                self.inputs['sfn'] = widgets.Text(
                    description='SFN: ',
                    value=self.data['Project Info']['sfn']
                )
                self.inputs['date'] = widgets.DatePicker(
                    description='Date:',
                    value=datetime.strftime(self.data['Project Info']['date'], "%B %d, %Y"),
                    disabled=False
                )
                self.inputs['pid'] = widgets.Text(
                    description='PID: ',
                    value=self.data['Project Info']['pid']
                )
                print('6')
        except KeyError as e:
            # Define input widgets - No Previous Data
            self.inputs['cty_rte_sec'] = widgets.Text(
                description='CTY-RTE-SEC: ',
                placeholder='Bridge CTY-RTE-SEC'
            )
            self.inputs['checker'] = widgets.Text(
                description='Checked By: ',
                placeholder="Employee's Initials"
            )
            self.inputs['sfn'] = widgets.Text(
                description='SFN: ',
                placeholder="Enter " 'multiple' " if more than one"
            )
            self.inputs['date'] = widgets.DatePicker(
                description='Date:',
                value=date.today(),
                disabled=False
            )
            self.inputs['pid'] = widgets.Text(
                description='PID: ',
                placeholder="Project PID"
            )

        # Define Load button
        self.load_button = widgets.Button(
            description="Load",
            button_style='primary',
            tooltip="Click to load project info",
            icon="check"
        )
        self.load_button.on_click(self.load_project_info)

        # Define submit button
        self.submit_button = widgets.Button(
            description="Submit",
            button_style='success',
            tooltip="Click to submit project info",
            icon="check"
        )
        self.submit_button.on_click(self.update_project_info)  # Attach callback

    def show_project_inputs(self):
        # Display all widgets and button
        display(
            self.inputs['pid'],
            self.inputs['cty_rte_sec'],
            self.inputs['sfn'],
            self.inputs['checker'],
            self.inputs['date'],
            self.load_button,
            self.submit_button
        )

    def load_project_info(self, b):
        """
        Loads the project info from a JSON file and populates the form values.
        """
        documents_path = Path(os.path.expanduser("~/Documents/Reviews"))
        json_file_path = documents_path / f"{self.inputs['pid'].value}/{self.inputs['pid'].value}.json"

        try:
            with open(json_file_path, "r") as json_file:
                project_info = json.load(json_file)
                self.data = project_info
                print(f"Loaded Project Info: {self.data}")

                # Populate the form inputs dynamically
                for key, value in self.data['Project Info'].items():
                    if key in self.inputs:
                        if key == 'date':
                            self.inputs[key].value = datetime.strptime(value, "%B %d, %Y")
                        else:
                            self.inputs[key].value = value
        except Exception as e:
            print(f"Error loading project info: {e}")

    def update_project_info(self, button=None):
        """
        Update `self.data` with the current values of the project info inputs.
        This method is triggered when the Submit button is clicked.
        """
        self.data['Project Info'] = {
            'cty_rte_sec': self.inputs['cty_rte_sec'].value,
            'checker': self.inputs['checker'].value,
            'date': self.inputs['date'].value.strftime('%B %d, %Y') if self.inputs['date'].value else "No date selected",
            'sfn': self.inputs['sfn'].value,
            'pid': self.inputs['pid'].value
        }
        print("Project Info Updated:", self.data['Project Info'])

        # Check if the folder and json file for this PID Exists
        if os.path.exists(f"Documents/Reviews/{self.data['Project Info']['pid']}.json"):
            print("Project Info Exists")
        else:
            generate_project_info(self.data, self.data['Project Info']['pid'])

    def get_project_scope(self):
        """
        Display widgets for project scope and handle user inputs for scope.

        There are three Primary Categories of Scope:
            Temporary Works,
            Superstructure, and
            Substructure.

        Each of these gets their own button and selection list defined here. When the buttons
        are clicked, the corresponding list stored in data['Scope'] is updated.
        """

        # Initialize widget for temporary works
        temporary_works = widgets.SelectMultiple(
            options=[
                None,
                'Shoring',
                'Sheeting',
                'Cofferdams'
            ],
            value=[],  # Defaults to an empty selection
            description='Select: ',
            rows=4,
            disabled=False
        )

        superstructure_work = widgets.SelectMultiple(
            options=[
                None,
                'Slab',
                'Prestressed Concrete Box Beams',
                'Prestressed Concrete I-Beams',
                'Steel Stringers',
                'Railing/Fence',
                'Bearings',
                'Deck Joints',
                'Deck Drainage',
                'Utilities',
                'Structure Grounding',
                'Approach Slab'
            ],
            value=[],
            description='Select: ',
            rows=12,
            disabled=False
        )

        substructure_work = widgets.SelectMultiple(
            options=[
                None,
                'Piers',
                'Abutments',
                'Drilled Shafts'
            ],
            value=[],
            description='Select: ',
            rows=4,
            disabled=False
        )

        # Define submit button for temporary works
        scope_submit_button = widgets.Button(
            description="Save Scope",
            button_style='primary',
            tooltip="Click to save Scope Components",
            icon="check"
        )

        # Callback to save scope data for temporary works
        def save_temp_works(button=None):
            if temporary_works.value == (None,):
                self.data['Scope']['Temp_Works'] = None
            else:
                self.data['Scope']['Temp_Works'] = {x: {} for x in list(temporary_works.value)}

        def save_superstructure(button=None):
            if superstructure_work.value == (None,):
                self.data['Scope']['Superstructure'] = None
            else:

                self.data['Scope']['Superstructure'] = {x: {} for x in list(superstructure_work.value)}

        def save_substructure(button=None):
            if substructure_work.value == (None,):
                self.data['Scope']['Substructure'] = None
            else:
                self.data['Scope']['Substructure'] = {
                    x: {} for x in list(substructure_work.value)
                }

        def save_all_3(event=None):
            save_temp_works()
            save_superstructure()
            save_substructure()

        scope_submit_button.on_click(save_all_3)

        # Display the widget and the corresponding button
        print('Does the project involve any temporary works? Select all that apply.')
        display(temporary_works)

        print('\n===============================Superstructure===============================\n')

        print('Select the superstructure components included in the project scope.')
        display(superstructure_work)

        print('\n================================Substructure================================\n')

        print('Select the substructure components included in the project scope.')
        display(substructure_work, scope_submit_button)

    def get_detailed_scope(self):
        temp_list = []
        try:
            if self.data['Scope']['Superstructure']:
                if 'Steel Stringers' in self.data['Scope']['Superstructure']:
                    steel_stringers = steel_stringer_details(self)
                    temp_list.append(('Superstructure', 'Steel Stringers', steel_stringers))
                if 'Railing/Fence' in self.data['Scope']['Superstructure']:
                    railings = railing_details(self)
                    temp_list.append(('Superstructure', 'Steel Stringers', railings))
                if 'Bearings' in self.data['Scope']['Superstructure']:
                    print('Bearings Question')
                if 'Deck Joints' in self.data['Scope']['Superstructure']:
                    print('Deck Joints Question')
                if 'Deck Drainage' in self.data['Scope']['Superstructure']:
                    print('Deck Drainage Question')

            if self.data['Scope']['Substructure']:
                if 'Piers' in self.data['Scope']['Substructure']:
                    print('Piers Question')
                if 'Abutments' in self.data['Scope']['Substructure']:
                    print('Abutments Question')

            details_submit_button = widgets.Button(
                description="Save Detailed Scope",
                button_style='primary',
                tooltip="Click to save Detailed Scope Components",
                icon="check"
            )

            def save_detailed_scope(button=None):
                for entry in temp_list:
                    self.data['Scope'][entry[0]][entry[1]] = entry[2].value

            details_submit_button.on_click(save_detailed_scope)

            display(details_submit_button)

        except KeyError as e:
            print('Error occured, this is usually from not saving one of the above values, like:', e,
                  '\nAfter correcting the error, rerun this cell by selecting it and pressing Shift+Enter')


def check_if_review_folder_exists():
    # Path to the user's Documents folder
    documents_path = os.path.expanduser("~/Documents")

    # Path to the Reviews folder
    reviews_folder = os.path.join(documents_path, "Reviews")

    # Check if the folder exists
    if not os.path.exists(reviews_folder):
        print("generating documents folder...")
        # Create the Reviews folder
        os.makedirs(reviews_folder)
    else:
        pass

def generate_project_info(data, pid):
    """
    Ensures that a folder for the entered PID exists in the user's Documents folder.
    If it doesn't exist, create it.
    """
    documents_path = Path(os.path.expanduser("~/Documents/Reviews"))
    pid_folder_path = documents_path / pid

    # Check if the folder exists and create it and the json file if not
    if not os.path.exists(pid_folder_path):
        print(f"Generating folder for PID '{pid}' in Documents...")
        os.makedirs(pid_folder_path)
    else:
        pass

    # Create/overwrite the JSON file on submittal of Project Data
    file_path = f"{pid}.json"
    print(pid_folder_path / file_path)

    with open(pid_folder_path / file_path, "w") as json_file:
        json.dump(data, json_file)  # Writes an empty JSON object
        print(f"JSON file Updated at: {pid_folder_path / file_path}")

def steel_stringer_details(checklist):
    steel_stringers = widgets.SelectMultiple(
        options=[
            'Rolled',
            'Plate',
        ],
        value=[],
        description='Select: ',
        rows=2,
        disabled=False
    )

    print('Select the type of steel stringers included in the project scope.')
    display(steel_stringers)

    return steel_stringers

def railing_details(checklist):
    railing = widgets.SelectMultiple(
        options=[
            'Deep Beam Railing',
            'Twin Steel Tube Railing',
            'Sidewalk Railing with Concrete Parapet',
            'Parapet Type Railing',
            'Parapet and Fence Type Railing'
        ],
        value=[],
        description='Select: ',
        rows=6,
        disabled=False
    )

    print('Select the type of steel stringers included in the project scope.')
    display(railing)

    return railing
