import ipywidgets as widgets
from IPython.display import display
from datetime import date


class Stage2StructuralChecklist:
    """
    Manages and organizes the creation of a structural checklist for Stage 2 projects.

    This class provides mechanisms to initialize, configure, and update project-specific
    checklists, allowing users to input project details, submit them through interactive
    widgets in Jupyter Lab, and manage project review data effectively.
    """
    def __init__(self):
        # Initialize to store widgets and data
        self.inputs = {}  # Stores the input widgets dynamically
        self.data = {'Scope': {}}  # Stores the data with `Scope` initialized as a dictionary

    def create_project_info_inputs(self):
        """Create input fields for project info and a submit button."""
        # Define input widgets
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

        # Define submit button
        self.submit_button = widgets.Button(
            description="Submit",
            button_style='primary',
            tooltip="Click to submit project info",
            icon="check"
        )
        self.submit_button.on_click(self.update_project_info)  # Attach callback

        # Display all widgets and button
        display(
            self.inputs['cty_rte_sec'],
            self.inputs['checker'],
            self.inputs['date'],
            self.inputs['sfn'],
            self.inputs['pid'],
            self.submit_button
        )

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

    def get_project_scope(self):
        """Display widgets for project scope and handle user inputs for scope.

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
                'Cofferdams',
                'Water Diversion'
            ],
            value=[],  # Defaults to an empty selection
            description='Select: ',
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

        print('\n===============================Substructure===============================\n')

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