import os
import json
import requests
from pathlib import Path

MIDAS_API_KEY = ''


def get_api_key(path_override=None):
    """
    Retrieve the API key from the secrets.json file in the civilpy directory

    Parameters
    -------
    path_override : the path where the secrets.json file is located

    Returns
    -------
    None - Sets a global variable for the module
    """
    global MIDAS_API_KEY

    if path_override is None:
        try:
            civilpy_secrets_path = Path(os.getcwd()).parent.parent.parent / 'secrets.json'
            with open(civilpy_secrets_path, 'r') as f:
                data = json.load(f)
                MIDAS_API_KEY = data['MIDAS_API_KEY']

        except FileNotFoundError as e:
            print(''''
                    Could not call the MIDAS API, ensure it\'s running and your key is correctly
                    Stored in your secrets.json file located at the following location:
                    ''')
            print(f"{e}")
    else:
        try:
            with open(path_override, 'r') as f:
                data = json.load(f)
                MIDAS_API_KEY = data['MIDAS_API_KEY']

        except FileNotFoundError as e:
            print(''''
                    Could not call the MIDAS API, ensure it\'s running and your key is correctly
                    Stored in your secrets.json file located at the following location:
                    ''')
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

        print(method, command, response.status_code)
        return response.json()
    except NameError as not_defined:
        print(''''
        Could not call the MIDAS API, ensure it\'s running and your key is correctly
        Stored in your secrets.json file located at the following location:
        ''')
        print(f"{not_defined}")


def convert_units(to: str) -> None:
    # Get the current list of nodes in midas
    nodes = midas_api('GET', "db/node")

    # Go through every node and multiply/divide depending on need
    for index_value in nodes['NODE']:
        print(index_value, end=': ')
        for xyz_value in nodes['NODE'][index_value]:
            print(f"{xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            if to == 'feet':
                nodes['NODE'][index_value][xyz_value] *= 12  # Convert from inches to feet
                print(f"Updated to {xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            elif to == 'inches':
                nodes['NODE'][index_value][xyz_value] *= 12  # Convert from inches to feet
                print(f"Updated to {xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            else:
                print('Please specify units to convert to ("feet"/"inches")')
                print('\n')

                # MidasAPI expects the first key in the values to be 'Assign'
                nodes['Assign'] = nodes.pop('NODE')

                # Send the updated values back to midas
                midas_api('PUT', "db/node", nodes)