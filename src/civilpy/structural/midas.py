import os
import json
import requests
from pathlib import Path
from civilpy.general import units

analysis_results_request = {
    "Argument": {
        "TABLE_NAME": "BeamForce",
        "TABLE_TYPE": "BEAMFORCE",
        "EXPORT_PATH": Path(os.getcwd()) / 'output.json',
        "UNIT": {
            "FORCE": "KIPS",
            "DIST": "FT"
        },
        "STYLES": {
            "FORMAT": "Default",
            "PLACE": 12
        },
        "COMPONENTS": [
            "Elem",
            "Load",
            "Part",
            "Axial",
            "Shear-y",
            "Shear-z",
            "Torsion",
            "Moment-y",
            "Moment-z"
        ],
        "NODE_ELEMS": {
            "KEYS": [
                "310to536"
            ]
        },
        "LOAD_CASE_NAMES": [
            "DL(CB)",
            "Moving Load Case(MV:all)"
        ],
        "PARTS": [
            "Part I",
            "Part 1/4",
            "Part 2/4",
            "Part 3/4",
            "Part J"
        ]
    }
}

MIDAS_API_KEY = ''


def get_api_key(secrets_path=None):
    """
    Retrieve the API key from the secrets.json file in the civilpy directory

    Parameters
    -------
    secrets_path : the path where the secrets.json file is located

    Returns
    -------
    None - Sets a global variable for the module
    """
    global MIDAS_API_KEY

    if secrets_path is None:
        try:
            secrets_path = Path(os.getcwd()).parent.parent / 'secrets.json'
            with open(secrets_path, 'r') as f:
                data = json.load(f)
                MIDAS_API_KEY = data['MIDAS_API_KEY']

        except FileNotFoundError as e:
            print(f'Could not call the MIDAS API, ensure it\'s running and your key is correctly')
            print(f'Stored in your secrets.json file located at the following location: {secrets_path}')
            print(f"{e}")
    else:
        try:
            with open(secrets_path, 'r') as f:
                data = json.load(f)
                MIDAS_API_KEY = data['MIDAS_API_KEY']

        except FileNotFoundError as e:
            print(f'Could not call the MIDAS API, ensure it\'s running and your key is correctly')
            print(f'Stored in your secrets.json file located at the following location: {secrets_path}')
            print(f"{e}")


# function for MIDAS Open API
def midas_api(method, command, body=None):
    """
    Make a request to the MIDAS API and return the
    response as a JSON object

    Parameters
    ----------
    method: str - 'GET', 'PUT', 'POST' or 'DELETE'
    command: str - The particular method within the API you want
        to target, such as 'db/elem' for the elements you want to access
    body: dict - The body of the request you want to send to the api, usually contains
        the values you want MIDAS to update with

    Returns
    -------
    response.json - the response from the MIDAS API
    """
    if MIDAS_API_KEY:
        pass
    else:
        get_api_key()
    base_url = "https://moa-engineers.midasit.com:443/civil/"
    mapi_key = MIDAS_API_KEY

    url = base_url + command
    headers = {
        "Content-Type": "application/json",
        "MAPI-Key": mapi_key
    }

    try:
        if method.upper() == "POST":
            response = requests.post(url=url, headers=headers, json=body)
        elif method.upper() == "PUT":
            response = requests.put(url=url, headers=headers, json=body)
        elif method.upper() == "GET":
            response = requests.get(url=url, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url=url, headers=headers)
        else:
            response = ''
            print('Invalid method, please use one of GET, POST, PUT, or DELETE')

        return response.json()
    except NameError as not_defined:
        print(''''
        Could not call the MIDAS API, ensure it\'s running and your key is correctly
        Stored in your secrets.json file located at the following location:
        ''')
        print(f"{not_defined}")


def convert_node_units(from_units: str = None, to_units: str = None, in_place: bool = True) -> None:
    """
    Converts the existing nodes from one unit system to another, for instance if you import
    a dxf file that was drawn in feet, but your midas units were set to inches,
    Parameters
    ----------
    from_units: str = The units the drawing is currently in ie 'inches' will grab them from midas if None
    to_units: str = The desired units to convert the drawing to, if None, will not run
    in_place: bool = Whether you want the function to push the data to the midas, or just return the updated values

    Returns
    -------
    None - Converts the units in the open model to the desired units
    nodes - if in_place is False
    """
    # Get the current list of nodes in midas
    nodes = midas_api('GET', "db/node")

    if from_units is None:
        units_api_response = midas_api('GET', "db/unit")
        from_units = units_api_response['UNIT']['1']['DIST'].lower()
    elif to_units is None:
        print('Please specify units to convert to ("feet"/"inches")')
        print('\n')

    # Go through every node and multiply/divide depending on need
    for index_value in nodes['NODE']:
        print(index_value, end=': ')
        for xyz_value in nodes['NODE'][index_value]:
            print(f"{xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            conversion_factor = (1 * units[from_units]).to(units[to_units]).magnitude
            nodes['NODE'][index_value][xyz_value] /= conversion_factor
            print(f"Updated to {xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
        print()

    # MidasAPI expects the first key in the values to be 'Assign'
    nodes['Assign'] = nodes.pop('NODE')

    if in_place:
        # Send the updated values back to midas
        midas_api('PUT', "db/node", nodes)
    else:
        return nodes


def get_elements():
    elements = midas_api('GET', 'db/elem')
    return elements


def get_nodes():
    nodes = midas_api('GET', 'db/node')
    return nodes


def get_materials():
    materials = midas_api('GET', 'db/matl')
    return materials


def get_sections():
    sections = midas_api('GET', 'db/sect')
    return sections


def get_static_loads():
    static_loads = midas_api('GET', 'db/stld')
    return static_loads


def get_units():
    current_units = midas_api('GET', 'db/unit')
    return current_units


def get_supports():
    support_definitions = midas_api('GET', 'db/cons')
    return support_definitions


def get_elements_by_section_index(section_index: int = None):
    """
    Returns a dictionary containing all elements of the midas model that match the section index

    Parameters
    ----------
    section_index: int = The index value of the section you want to search the elements for

    Returns
    -------
    return_dict: A dictionary containing all elements of the midas model that match the section
        specified
    """
    return_dict = {'ELEM': {}}
    elements = get_elements()

    if section_index is not None:
        for key in elements['ELEM']:
            if elements['ELEM'][key]['SECT'] == section_index:
                return_dict['ELEM'][key] = elements['ELEM'][key]
    else:
        print('You must specify a section by it\'s index')

    return return_dict


def get_elements_by_material_index(material_index: int = None):
    """
    Get the elements of a model by specifying a material index value
    Parameters
    ----------
    material_index: int = Index of the material you want to sort by in str format

    Returns
    -------
    return_dict: dict = The elements of a model that match the material specified
    """
    return_dict = {'ELEM': {}}
    elements = get_elements()

    if material_index is not None:
        for keys in elements['ELEM']:
            if elements['ELEM'][keys]['MATL'] == material_index:
                return_dict['ELEM'][keys] = elements['ELEM'][keys]
    else:
        print('You must specify a material by it\'s index')

    return return_dict


def setup_output_directory(output_directory: str = os.getcwd()):
    if os.path.isdir(Path(output_directory) / 'output'):
        print('Output directory already exists')
    else:
        print(f"Directory doesn't exist, creating at {Path(output_directory) / 'output'}")
        os.mkdir(output_directory)


setup_output_directory()